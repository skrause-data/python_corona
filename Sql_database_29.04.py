'''
Path für Datenbank erstellt.
------------------------------------>
Datenbank zum Speichern und Aktualisieren von Fallzahl-Nummern nach Datum.
------------------------------------>
Land: Germany, Italy, Switzerland, France, Spain, Austria, Netherlands
'''

import os
import sqlite3

PATH = os.path.join(os.path.dirname(__file__), "mydatabase.sqlite3")

class Db():
    
    def __init__(self):
        '''
        Stellt eine Verbindung zur Datenbank her
        bzw. erstellt eine Datenbank wenn nicht vorhanden
        '''
        self.connection = sqlite3.connect(PATH)

        try:
            self.new_db()
        except sqlite3.OperationalError:
            pass
        print(self.new_db)
    
    def new_db(self):
        '''
        legt neue Datenbank an
        '''
        Land = ['germany', 'italy', 'switzerland', 'france', 'spain', 'austria', 'netherlands']
        cursor = self.connection.cursor()
        for element in Land:
            
            query_new_table= f'''
                CREATE TABLE {element} (id, Fallzahl ,Tag);'''
       
            cursor.execute(query_new_table)
           
        
        
    def new_datenbank(self, Fallzahl, Tag):   
         '''
         speicher ein neus Data in der Datenbank
        '''
         cursor = self.connection.cursor()
         Land = ['germany', 'italy', 'switzerland', 'france', 'spain', 'austria', 'netherlands']
         for element in Land:
            
             query_insert_new_data = f'''
                 INSERT INTO {element} (id, Fallzahl, Tag)  
                 VALUES (NULL, {Fallzahl}, '{Tag}');'''
        
             
             cursor.execute(query_insert_new_data)                      
             self.connection.commit()
     
        
        
    def select_all_from_db(self, table, condition="True=True"):
        cursor = self.connection.cursor()  
        select_from_db = f'''
            SELECT * FROM "{table}"
            WHERE {condition}; 
            '''
        cursor.execute(select_from_db)
        result = cursor.fetchall()
        return result
       
    
    
    def update_table_in_db(self, table, numbers, value, condition="True=True"):
        cursor = self.connection.cursor()  
        query_update_table_in_db = f'''
            UPDATE "{table}"
                SET "{numbers}" = "{value}"
                WHERE {condition};
            '''
        cursor.execute(query_update_table_in_db)
        self.connection.commit()
       
        
    def close_db(self):
        self.connection.close()
        
    
Land_databank = Db()
Land_databank.new_datenbank(50000, '2020-04-28')
result = Land_databank.select_all_from_db('france')
print(result)      
        

    





