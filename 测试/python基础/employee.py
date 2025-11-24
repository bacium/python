# 已有员工数据
employee_records = {
    "1001": {'name': 'Alice', 'age': 25, 'position': 'Manager'},
    "1002": {'name': 'Bob', 'age': 30, 'position': 'Engineer'}
}


# 根据给定的员工工号查询员工信息
def query_employee(id):
    target_employee = employee_records[id]
    print(target_employee)
    return f"员工姓名:{target_employee["name"]},员工年龄:{target_employee["age"]},员工职位:{target_employee["position"]}"


# 增加员工信息
def add_employee(info):
    employee_records[info["id"]] = info["values"]
    print(employee_records)
    return f"新增编号:{employee_records[info["id"]]}成功"


def del_employee(id):
    message = employee_records[id]
    del employee_records[id]
    return f"删除员工{message["name"]}成功"


if __name__ == "__main__":
    em = query_employee("1001")
    print(em)
    info = {
        "id": "1003",
        "values": {'name': '李白', 'age': 16, 'position': '老六'}
    }
    add = add_employee(info)
    remove = del_employee("1003")
    print(remove)
