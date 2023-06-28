##from __future__ import print_function
import json
import pandas as pd
import pdb
import datetime

def dict_generator(indict, pre=None):
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            #pdb.set_trace()
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre+[key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                value_list = str(value)
                if value_list.find("{") > 0:
                    if len(value) == 0:                   
                        yield pre+[key, '[]']
                    else:
                        for v in value:
                            for d in dict_generator(v, pre + [key]):
                                yield d
                else:
                    yield pre + [key, value]
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre+[key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        print("Not dict")
        yield indict

##if __name__ == "__main__":
##    sJOSN = open('test.json', encoding='utf-8').read()
##    sValue = json.loads(sJOSN)
##    pdb.set_trace()
##    for num in sValue:
##        for i in dict_generator(num):
##            print('.'.join('%s' %id for id in i[0:-1]), ':', (i[-1]))

 
def  get_all_record_list(read_file_name):
##  每一个对象的json的dict  转换为list
        all_record_list = []
        names = locals()
        dnum = 1
        columns_set = set()
        num = 0
        KEY_INDEX_NAME =  'name'
        
        fh = open(read_file_name,'r')
        sJOSN = fh.read()
        sValue = json.loads(sJOSN)

        for jnum in sValue:
            names['record_list%dnum' % dnum] = {}
            for line in dict_generator(jnum):
                key = '.'.join('%s' %id for id in line[0:-1])
                value = line[-1]
                columns_set.add(key)
                
                if key == KEY_INDEX_NAME and num > 0:
##                    all_record_list.append(record_dict.copy())
                    names['record_list%dnum' % dnum].clear()
                    names['record_list%dnum' % dnum][key] = value
                else:
                    names['record_list%dnum' % dnum][key] = value
                num = num + 1
            
            all_record_list.append(names['record_list%dnum' % dnum])
                
        return all_record_list,columns_set
 
 
def list_convert_df(all_record_list,columns_set):
##        每一个对象的json的dict  转换为list,并且把缺失的字段补上。然后转换为df    
        record_list = []
        combin_list = []
        
        for  record in  all_record_list:
            for column in columns_set:
                record_list.append(record.get(column,''))
            combin_list.append(record_list.copy())    
            record_list.clear()

        df = pd.DataFrame(combin_list,columns = list(columns_set))
        
        print ("write over")  
        return df
 
def change_id_to_first(df): 
##      把每一个小的json的id转换为df之后，调到最前头。
        KEY_ID_NAME = 'name'
        df_id = df[KEY_ID_NAME]
        df = df.drop(KEY_ID_NAME,axis=1)
        df.insert(0,KEY_ID_NAME,df_id)
        return df
 
    
if __name__ == "__main__":
       
    all_record_list,columns_set = get_all_record_list('test.json')
    
    
    df = list_convert_df(all_record_list,columns_set)
    df = df.sort_index(axis=1,ascending=True)
    df = change_id_to_first(df)
    
    
##    print(df)
    
    currentTime = datetime.datetime.now()
    df.to_excel('builtin_security_event_config'+currentTime.strftime("%Y%m%d")+'.xlsx',sheet_name='sheet1',index=False)
  
 
 
 
