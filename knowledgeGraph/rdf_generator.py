import pandas as pd
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD
import sqlalchemy
from sqlalchemy import MetaData, inspect
import json
from database.db import get_database_schema, db_config
from dotenv import load_dotenv
import os
import math

username = 'postgres'
password = 'postgre'
database_name = 'AndeanMythology'
host = 'localhost'
port = '5432'  

connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

def generate_ttl(output_path="output.ttl"):
    db_url = connection_string
    engine = sqlalchemy.create_engine(db_url)

    metadata = MetaData()
    metadata.reflect(bind=engine)

    inspector = inspect(engine)
    knowledge_graph = Graph()

    mythology_ns = Namespace("http://example.org/mythology/")
    knowledge_graph.bind("rdf", RDF)
    knowledge_graph.bind("rdfs", RDFS)

    def generate_label(table, row):
        if len(row) > 1:  
            return f"{table}_{str(row.iloc[1])}" 
        return f"Resource {row.iloc[0]}"

    schema = get_database_schema(db_config)
    schema_dict = json.loads(schema)

    for table_name, table_info in schema_dict.items():
        knowledge_graph.add((mythology_ns[table_name], RDF.type, RDFS.Class))
        knowledge_graph.add((mythology_ns[table_name], RDFS.label, Literal(table_name, datatype=XSD.string)))
        
        for column in table_info['columns']:
            column_name = column['column_name']
            data_type = column['data_type']
            property_uri = mythology_ns[f"{table_name}_{column_name}"]
            knowledge_graph.add((property_uri, RDF.type, RDF.Property))
            knowledge_graph.add((property_uri, RDFS.label, Literal(column_name, datatype=XSD.string)))
            knowledge_graph.add((property_uri, RDFS.range, Literal(data_type, datatype=XSD.string)))
            knowledge_graph.add((property_uri, RDFS.domain, mythology_ns[table_name]))


    for table in metadata.tables.keys():
        df = pd.read_sql_table(table, engine)
        foreign_keys = inspector.get_foreign_keys(table)

        for _, row in df.iterrows():
            subject = URIRef(mythology_ns[f"{table}/{table}{row.iloc[0]}"])
            knowledge_graph.add((subject, RDF.type, mythology_ns[table]))

            label = generate_label(table, row)
            knowledge_graph.add((subject, RDFS.label, Literal(label, datatype=XSD.string)))

            for column in df.columns:
                value = row[column]
                if (isinstance(value, str) or not math.isnan(value)):

                    if(isinstance(value, float)):
                        value = int(value)

                    if column in [fk['constrained_columns'][0] for fk in foreign_keys]:
                        ref_table = [fk['referred_table'] for fk in foreign_keys if fk['constrained_columns'][0] == column][0]
                        ref_subject = URIRef(mythology_ns[f"{ref_table}/{ref_table}{value}"])
                        knowledge_graph.add((subject, mythology_ns[f"has_{ref_table}"], ref_subject))
                    else:
                        if isinstance(value, str):
                            knowledge_graph.add((subject, mythology_ns[f"{table}_{column}"], Literal(value, datatype=XSD.string)))
                        elif isinstance(value, (int, float)):
                            knowledge_graph.add((subject, mythology_ns[f"{table}_{column}"], Literal(value, datatype=XSD.double)))
                        else:
                            knowledge_graph.add((subject, mythology_ns[f"{table}_{column}"], Literal(str(value), datatype=XSD.string)))

    knowledge_graph.serialize(destination=output_path, format="turtle")
    return output_path

generate_ttl("output.ttl")