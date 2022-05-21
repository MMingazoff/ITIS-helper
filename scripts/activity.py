import openpyxl

if __name__ == "__main__":
    book = openpyxl.open("activ.xlsx", data_only = True)
    book2 = openpyxl.open("activ2.xlsx", data_only = True)
    sheets=[book.worksheets[1],book.worksheets[2]]
    sheets2=[book2.worksheets[0]]
    data={}
    for sheet in sheets:
          for name,balls in sheet.iter_rows(min_row=6,min_col=2,max_col=3):
            data[name.value]= balls.value + data.get(name.value,0)
    for name,balls in sheets2[0].iter_rows(min_row=2,min_col=2,max_col=3):
        data[name.value]=balls.value + data.get(name.value,0)
    list_of_data = []
    for key in data:
        if key!=None:
            list_of_small_data=[key,data[key]]
            list_of_data.append(list_of_small_data)
    n=1
    
    list_of_data.sort(key=lambda i: i[n],reverse=True)
    i = 1
    for step in list_of_data:
        step=step.append(f"№{i}")
        i+=1
    for person in data:
        for info in list_of_data:
            data.update(person = (info[1],info[2]))
    data2 ={}
    for info in list_of_data:
        data2[info[0]] = (info[1],info[2])
    print(data2)