import pandas as pd
import docx
import os
import sys
from rdflib import Graph, Literal, RDF, URIRef
from datetime import date


class Converter():
    """
    Trieda konvertora, obsahuje všetky funkcie programu určené na konverziu,
        alebo zapisovanie metaúdajov


    Attributes
    ----------
    inputPath : str
        cesta ku vstupnému súboru
    metadataPath : str
        cesta k súboru metaúdajov
    outputPath : str
        cesta k výstupnému súboru
    format : str
        formát výstupného súboru (ttl, xml, csv)

    Methods
    -------
    CSVtoRDF()
        konverzia súboru CSV na súbor RDF
    RDFtoCSV()
        konverzia súboru RDF na súbor CSV
    WriteMetadata()
        pripísanie metadát k výstupnému súboru
    ReadMetadata(filePath)
        prečítanie metadát zo súboru "filePath"
    """

    def __init__(self):
        self.inputPath = ""
        self.metadataPath = ""
        self.outputPath = ""
        self.format = "ttl"

    def set_inputPath(self, path):
        self.inputPath = path

    def set_metadataPath(self, path):
        self.metadataPath = path

    def set_outputPath(self, path):
        self.outputPath = path

    def set_format(self, format):
        self.format = format

    def resource_path(self, relative_path):
        """
        Pomocná funkcia na správne načítanie obrázkov v používateľskom rozhraní. 
        """

        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def CSVtoRDF(self):
        """
        Prekonvertuje CSV súbor umiestnený v "inputPath" na výstupný RDF súbor
            podľa formátu "format" a umiestni ho na "outputPath". Potom spustí
            funkciu WriteMetadata().
        """

        try:
            df=pd.read_csv(self.inputPath,sep=",",quotechar='"')
            print(df.head())
        except:
            return -1

        columns = df.columns.values.tolist()[2:]
        print(columns)
        g = Graph()

        for _, row in df.iterrows():
            uri = URIRef(row["URI"])
            g.add(( uri, RDF.type, URIRef(row["Type"]) ))
            for col in columns:    
                g.add(( uri, URIRef(col), Literal(row[col]) ))       

        try:
            g.serialize(destination=self.outputPath,format=self.format)
        except:
            return -2

        return self.WriteMetadata()

    def RDFtoCSV(self):
        """
        Prekonvertuje RDF súbor umiestnený v "inputPath" na výstupný CSV súbor
           a umiestni ho na "outputPath". Potom spustí funkciu WriteMetadata().
        """

        g = Graph()
        try:
            g.parse(self.inputPath)
        except:
            return -1

        columnNames = list(map(str, g.predicates(unique=True)))
        df = pd.DataFrame(columns=columnNames)
    
        for s,p,o in g:
            df.at[str(s), str(p)] =  str(o)

        df.index.names = ['URI']
        df = df.rename(columns = {'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':'Type'})
        try:
            df.to_csv(self.outputPath)
        except:
            return -2

        return self.WriteMetadata()



    def WriteMetadata(self):
        """
        Pripíše metaúdaje k výstupnému súboru umiestnenému na "outputPath".
        """

        try:           
            with open(self.outputPath+':ADS', 'w+') as ads:
                today = date.today()
                ads.write("conversion_date="+today.strftime("%d.%m.%Y")+"\n")
                ads.write("conversion_tool=RDF_converter\n")
                ads.write("converted_from="+self.inputPath+"\n")
                ads.write("curent_user="+os.getlogin()+"\n")

                # If specified, append user metadata
                if(self.metadataPath != ''): 
                    if(self.metadataPath.split(".")[1] == 'txt'): 
                        with open(self.metadataPath, 'r') as f:
                            for line in f.readlines():
                                ads.write(line)
                                print(line)
                    elif(self.metadataPath.split(".")[1] == 'docx'): 
                        doc = docx.Document(self.metadataPath)
                        for p in doc.paragraphs:
                            ads.write(p.text+'\n')
                            print(p.text)
                    else:
                        return -3
        except:
            return -3
    
        return 1


    def ReadMetadata(filePath):
        """
        Vráti metaúdaje súboru umiestneného na "filePath".
        """

        try:
            with open(filePath+':ADS', 'r') as ads:
                return ads.readlines()
        except:
            return "Tento súbor neobsahuje metadáta."