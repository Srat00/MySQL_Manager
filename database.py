import pymysql
import pandas as pd
import getpass
from tabulate import tabulate

#    ______  ___         _______________ ______        ______  ___                                                
#    ___   |/  /_____  ____  ___/__  __ \___  /        ___   |/  /______ ________ ______ ________ ______ ________ 
#    __  /|_/ / __  / / /_____ \ _  / / /__  /         __  /|_/ / _  __ `/__  __ \_  __ `/__  __ `/_  _ \__  ___/
#    _  /  / /  _  /_/ / ____/ / / /_/ / _  /___       _  /  / /  / /_/ / _  / / // /_/ / _  /_/ / /  __/_  /    
#    /_/  /_/   _\__, /  /____/  \___\_\ /_____/       /_/  /_/   \__,_/  /_/ /_/ \__,_/  _\__, /  \___/ /_/     
#               /____/                                                                    /____/                 
#
#    MySQL Manager
#    CBNU Software Database Systems 22-2 
#    2022-11-06      2020039091 Rocky Eo

#Title
print("______  ___         _______________ ______ \n___   |/  /_____  ____  ___/__  __ \___  / \n__  /|_/ / __  / / /_____ \ _  / / /__  /  \n_  /  / /  _  /_/ / ____/ / / /_/ / _  /___\n/_/  /_/   _\__, /  /____/  \___\_\ /_____/\n           /____/                          \n                      2020039091 어록희        ")

#로그인
print("IP : ", end = "")
ip = input()
print("Port : ", end = "")
port = input()
print("User : ", end = "")
user = input()
password = getpass.getpass("Password : ")
print("Database : ", end = "")
database = input()

print("데이터베이스에 연결합니다...\n\n")

#연결 성공
try:
    sqlConnect = pymysql.connect(host=ip, port=int(port), user=user, password=password, db=database, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    print("데이터베이스에 연결되었습니다. 비정상적으로 종료할 경우 수정한 데이터가 유실될 수 있습니다.\n\n")
    
    cursor = sqlConnect.cursor()
    #메인메뉴
    while(True):
        print("\n어떤 작업을 하시겠습니까? \n 1. 데이터 삽입\n 2. 데이터 수정 \n 3. 데이터 삭제 \n 4. 데이터 검색 \n 0. 종료 \n\n >> ", end = "")
        select = input()
        
        #데이터 삽입
        if (int(select) == 1):
            print("\n테이블 명을 입력하십시오. \n >> ", end = "")
            table = input()
            while(True):
                print("\n삽입할 데이터를 입력하십시오. \n >> ", end = "")
                data = input()                
                quarry = "INSERT INTO " + table + " VALUES (" + data + ")"
                
                try:
                    cursor.execute(quarry)
                    print("\n데이터를 삽입했습니다. 계속 삽입하시려면 1을 입력해주십시오.\n >> ", end = "")
                    select = input()
                    if(select != '1'):
                        break
                except Exception as e:
                    print("\n데이터 삽입에 실패하였습니다. 데이터를 확인하십시오.", e, "\n\n")
        
        #데이터 수정
        elif (int(select) == 2):
            print("\n테이블 명을 입력하십시오. \n >> ", end = "")
            table = input()
            while(True):
                print("\n수정할 조건을 입력하십시오. 조건을 생략하면 전체 데이터가 수정됩니다! \n >> ", end = "")
                condition = input()
                
                print("\n수정할 데이터를 입력하십시오. \n >> ", end = "")
                data = input()
                
                if len(condition) == 0:
                    quarry = "UPDATE " + table + " SET " + data
                else:
                    quarry = "UPDATE " + table + " SET " + data + " WHERE " + condition
                
                try:
                    cursor.execute(quarry)
                    print("\n데이터를 수정했습니다. 계속 수정하시려면 1을 입력해주십시오.\n >> ", end = "")
                    select = input()
                    if(select != '1'):
                        break
                except Exception as e:
                    print("\n데이터 수정에 실패하였습니다. 데이터를 확인하십시오.", e, "\n\n")
            
        #데이터 삭제
        elif (int(select) == 3):
            print("\n테이블 명을 입력하십시오. \n >> ", end = "")
            table = input()
            while(True):
                print("\n삭제할 조건을 입력하십시오. 조건을 생략하면 전체 데이터가 삭제됩니다! \n >> ", end = "")
                condition = input()
                
                if len(condition) == 0: #조건이 없으면
                    quarry = "DELETE FROM " + table
                else:
                    quarry = "DELETE FROM " + table + " WHERE " + condition
        
                try:
                    cursor.execute(quarry)
                    print("\n데이터를 삭제했습니다. 계속 삭제하시려면 1을 입력해주십시오.\n >> ", end = "")
                    select = input()
                    if(select != '1'):
                        break
                except Exception as e:
                    print("\n데이터 삭제에 실패하였습니다. 조건을 확인하십시오.", e, "\n\n")
        
        #데이터 검색     
        elif (int(select) == 4):
            print("\n테이블 명을 입력하십시오. \n >> ", end = "")
            table = input()
            while(True):
                print("\n검색할 조건을 입력하십시오. 조건을 생략하면 전체 데이터가 검색됩니다! \n >> ", end = "")
                condition = input()
                
                if len(condition) == 0: #조건이 없으면
                    quarry = "SELECT * FROM " + table
                else:
                    quarry = "SELECT * FROM " + table + " WHERE " + condition
        
                try:
                    cursor.execute(quarry)
                    result = cursor.fetchall() #검색결과 불러오기
                    df = pd.DataFrame()
                    for row in result:
                        df = pd.concat([df, pd.DataFrame(row, index=[0])], axis=0) #Dictionary 형태로 불러들여온 데이터를 DataFrame으로 변환
                    
                    print(tabulate(df, headers='keys', tablefmt='psql', showindex=True)) #Tabulate를 사용하여 DataFrame을 테이블 형태로 출력
                    print('\n\n')
                    
                    print("\n데이터를 검색했습니다. 계속 검색하시려면 1를 입력해주십시오.\n >> ", end = "")
                    select = input()
                    if(select != '1'):
                        break
                        
                    
                except Exception as e:
                    print("\n데이터 조회에 실패하였습니다. 조건을 확인하십시오.", e, "\n\n")
                
        
        elif (int(select) == 0):
            while(True):
                print("\n수정사항을 저장하시겠습니까? Y/N")
                select = input()
                if(select == 'Y' or select == 'y'):
                    sqlConnect.commit()
                    print("\n수정사항이 저장되었습니다.")
                    break
                elif(select == 'N' or select == 'n'):
                    break
                else:
                    print("\n잘못된 입력입니다.")
                    
            print("\n\n프로그램을 종료합니다.")
            sqlConnect.close() # DB 연결 종료
            quit()
        
        else:
            print("\n잘못된 입력입니다. 다시 입력해주세요. \n >> ", end = "")
#연결 실패            
except Exception as e:
    print("\n데이터베이스와 연결중 오류가 발생했습니다. 프로그램을 종료합니다.", e)
    
    

