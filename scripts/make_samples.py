# Copyright 2024 Jheng-Hong Yang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pathlib
import shutil
import textwrap

base_dir = pathlib.Path("data")
if base_dir.exists():
    shutil.rmtree(base_dir)
base_dir.mkdir(parents=True, exist_ok=True)


def wjsonl(name, rows):
    with (base_dir / name).open("w", encoding="utf-8") as f:
        for r in rows:
            json.dump(r, f, ensure_ascii=False)
            f.write("\n")


# CONTACTS
contacts = [
    {
        "ContactID": "C001",
        "LastName": "王",
        "FirstName": "俊凱",
        "Email": "jk.wang@mototech.com.tw",
        "Mobile": "0912-345-678",
        "Preferred": "Email",
        "Department": "Sales",
        "Title": "業務主任",
        "Active": "Y",
        "Timezone": "Asia/Taipei",
    },
    {
        "ContactID": "C002",
        "LastName": "林",
        "FirstName": "雅婷",
        "Email": "yt.lin@mototech.com.tw",
        "Mobile": "0922-238-866",
        "Preferred": "LINE",
        "Department": "Marketing",
        "Title": "行銷經理",
        "Active": "Y",
        "Timezone": "Asia/Taipei",
    },
    {
        "ContactID": "C003",
        "LastName": "陳",
        "FirstName": "志宏",
        "Email": "zh.chen@mototech.com.tw",
        "Mobile": "0933-678-901",
        "Preferred": "Mobile",
        "Department": "R&D",
        "Title": "資深工程師",
        "Active": "Y",
        "Timezone": "Asia/Taipei",
    },
    {
        "ContactID": "C004",
        "LastName": "吳",
        "FirstName": "佩珊",
        "Email": "ps.wu@mototech.com.tw",
        "Mobile": "0955-112-233",
        "Preferred": "Email",
        "Department": "HR",
        "Title": "HR 副理",
        "Active": "Y",
        "Timezone": "Asia/Taipei",
    },
]

# Helper to find contact details
contact_map = {c["ContactID"]: c for c in contacts}

# CUSTOMERS with English-friendly columns
customers = [
    {
        "CustomerID": "CU001",
        "CompanyName": "台灣中鋼股份有限公司",
        "UBN": "30414175",
        "Type": "製造業",
        "Address": "成功二路 5 號",
        "City": "高雄市",
        "Region": "前鎮區",
        "PostalCode": "806",
        "Country": "台灣",
        "ContactID": "C001",
        "ContactName": contact_map["C001"]["FirstName"]
        + contact_map["C001"]["LastName"],
        "ContactTitle": contact_map["C001"]["Title"],
        "Email": "purchasing@csc.com.tw",
        "Phone": "07-331-1711",
        "Fax": "07-331-1712",
        "RegisteredDate": "2023-03-15",
        "Level": "A",
        "Status": "Active",
        "VIPFlag": "Y",
    },
    {
        "CustomerID": "CU002",
        "CompanyName": "台灣電力公司",
        "UBN": "03721530",
        "Type": "公用事業",
        "Address": "羅斯福路三段 242 號",
        "City": "台北市",
        "Region": "中正區",
        "PostalCode": "100",
        "Country": "台灣",
        "ContactID": "C002",
        "ContactName": contact_map["C002"]["FirstName"]
        + contact_map["C002"]["LastName"],
        "ContactTitle": contact_map["C002"]["Title"],
        "Email": "tender@taipower.com.tw",
        "Phone": "02-2365-1234",
        "Fax": "02-2365-1235",
        "RegisteredDate": "2023-05-20",
        "Level": "A",
        "Status": "Active",
        "VIPFlag": "Y",
    },
    {
        "CustomerID": "CU003",
        "CompanyName": "友達光電股份有限公司",
        "UBN": "38950976",
        "Type": "製造業",
        "Address": "中園路二段 1 號",
        "City": "桃園市",
        "Region": "中壢區",
        "PostalCode": "320",
        "Country": "台灣",
        "ContactID": "C003",
        "ContactName": contact_map["C003"]["FirstName"]
        + contact_map["C003"]["LastName"],
        "ContactTitle": contact_map["C003"]["Title"],
        "Email": "vendor@auo.com",
        "Phone": "03-500-8800",
        "Fax": "03-500-8801",
        "RegisteredDate": "2023-10-02",
        "Level": "B",
        "Status": "Active",
        "VIPFlag": "N",
    },
    {
        "CustomerID": "CU004",
        "CompanyName": "華碩電腦股份有限公司",
        "UBN": "23638777",
        "Type": "科技業",
        "Address": "立功街 150 號",
        "City": "台北市",
        "Region": "北投區",
        "PostalCode": "112",
        "Country": "台灣",
        "ContactID": "C004",
        "ContactName": contact_map["C004"]["FirstName"]
        + contact_map["C004"]["LastName"],
        "ContactTitle": contact_map["C004"]["Title"],
        "Email": "scm@asus.com",
        "Phone": "02-2894-3447",
        "Fax": "02-2894-3448",
        "RegisteredDate": "2024-01-11",
        "Level": "A",
        "Status": "Active",
        "VIPFlag": "N",
    },
    {
        "CustomerID": "PC001",
        "CompanyName": "台灣塑膠工業股份有限公司",
        "UBN": None,
        "Type": "製造業",
        "Address": "中正路 1 號",
        "City": "台南市",
        "Region": "仁德區",
        "PostalCode": "717",
        "Country": "台灣",
        "ContactID": None,
        "ContactName": None,
        "ContactTitle": None,
        "Email": None,
        "Phone": None,
        "Fax": None,
        "RegisteredDate": "2025-03-01",
        "Level": None,
        "Status": "Prospect",
        "VIPFlag": "N",
    },
    {
        "CustomerID": "PC002",
        "CompanyName": "鴻海精密工業股份有限公司",
        "UBN": None,
        "Type": "製造業",
        "Address": "中山路 66 號",
        "City": "新北市",
        "Region": "土城區",
        "PostalCode": "236",
        "Country": "台灣",
        "ContactID": None,
        "ContactName": None,
        "ContactTitle": None,
        "Email": None,
        "Phone": None,
        "Fax": None,
        "RegisteredDate": "2025-03-15",
        "Level": None,
        "Status": "Prospect",
        "VIPFlag": "N",
    },
    {
        "CustomerID": "PC003",
        "CompanyName": "聯發科技股份有限公司",
        "UBN": None,
        "Type": "科技業",
        "Address": "篤行一路 1號",
        "City": "新竹市",
        "Region": "東區",
        "PostalCode": "300",
        "Country": "台灣",
        "ContactID": None,
        "ContactName": None,
        "ContactTitle": None,
        "Email": None,
        "Phone": None,
        "Fax": None,
        "RegisteredDate": "2025-04-01",
        "Level": None,
        "Status": "Prospect",
        "VIPFlag": "N",
    },
]

# PRODUCTS
products = [
    {
        "ProductID": "P-IM15",
        "ProductName": "15 kW 三相感應馬達",
        "Category": "工業用馬達",
        "Model": "IM-15KW-220V",
        "Origin": "台灣",
        "ListPrice": 56000,
    },
    {
        "ProductID": "P-VFD22",
        "ProductName": "22 kW 變頻器",
        "Category": "工業控制",
        "Model": "VFD-22KW-3P",
        "Origin": "日本",
        "ListPrice": 45000,
    },
    {
        "ProductID": "P-IM55",
        "ProductName": "55 kW 三相感應馬達",
        "Category": "工業用馬達",
        "Model": "IM-55KW-380V",
        "Origin": "台灣",
        "ListPrice": 128000,
    },
    {
        "ProductID": "P-VFD7.5",
        "ProductName": "7.5 kW 變頻器",
        "Category": "工業控制",
        "Model": "VFD-7.5KW-3P",
        "Origin": "日本",
        "ListPrice": 18000,
    },
]

# ORDERS (add for VIP trend)
orders = [
    {
        "OrderID": "O2024-0201",
        "CustomerID": "CU002",
        "OrderDate": "2024-02-12",
        "ShipDate": "2024-03-02",
        "Status": "Closed",
        "TotalAmount": 590000,
        "Currency": "TWD",
        "Comments": "",
    },
    {
        "OrderID": "O2024-0601",
        "CustomerID": "CU002",
        "OrderDate": "2024-06-15",
        "ShipDate": "2024-07-05",
        "Status": "Closed",
        "TotalAmount": 880000,
        "Currency": "TWD",
        "Comments": "",
    },
    {
        "OrderID": "O2024-0901",
        "CustomerID": "CU002",
        "OrderDate": "2024-09-10",
        "ShipDate": "2024-10-05",
        "Status": "Closed",
        "TotalAmount": 1200000,
        "Currency": "TWD",
        "Comments": "",
    },
    {
        "OrderID": "O2025-0401",
        "CustomerID": "CU002",
        "OrderDate": "2025-04-20",
        "ShipDate": "2025-05-22",
        "Status": "Shipped",
        "TotalAmount": 1100000,
        "Currency": "TWD",
        "Comments": "",
    },
    {
        "OrderID": "O2025-0301",
        "CustomerID": "CU003",
        "OrderDate": "2025-05-02",
        "ShipDate": None,
        "Status": "InProcess",
        "TotalAmount": 2984000,
        "Currency": "TWD",
        "Comments": "",
    },
    {
        "OrderID": "O2024-0815",
        "CustomerID": "CU001",
        "OrderDate": "2024-08-15",
        "ShipDate": "2024-09-01",
        "Status": "Closed",
        "TotalAmount": 750000,
        "Currency": "TWD",
        "Comments": "Urgent delivery for new project",
    },
    {
        "OrderID": "O2023-0510",
        "CustomerID": "CU001",
        "OrderDate": "2023-05-10",
        "ShipDate": "2023-05-28",
        "Status": "Closed",
        "TotalAmount": 1211000,
        "Currency": "TWD",
        "Comments": "Phase 1 supply for plant upgrade",
    },
    {
        "OrderID": "O2023-1120",
        "CustomerID": "CU001",
        "OrderDate": "2023-11-20",
        "ShipDate": "2023-12-10",
        "Status": "Closed",
        "TotalAmount": 740000,
        "Currency": "TWD",
        "Comments": "Additional motors for expansion",
    },
    {
        "OrderID": "O2024-0315",
        "CustomerID": "CU004",
        "OrderDate": "2024-03-15",
        "ShipDate": "2024-04-02",
        "Status": "Closed",
        "TotalAmount": 460000,
        "Currency": "TWD",
        "Comments": "New server room cooling system motors",
    },
    {
        "OrderID": "O2024-1005",
        "CustomerID": "CU004",
        "OrderDate": "2024-10-05",
        "ShipDate": "2024-10-25",
        "Status": "Closed",
        "TotalAmount": 346000,
        "Currency": "TWD",
        "Comments": "R&D lab equipment",
    },
]

# ORDER LINES (subset)
order_lines = [
    {
        "LineID": 1,
        "OrderID": "O2024-0201",
        "ProductID": "P-IM15",
        "Qty": 5,
        "UnitPrice": 56000,
    },
    {
        "LineID": 2,
        "OrderID": "O2024-0201",
        "ProductID": "P-VFD22",
        "Qty": 3,
        "UnitPrice": 45000,
    },
    {
        "LineID": 3,
        "OrderID": "O2024-0601",
        "ProductID": "P-IM15",
        "Qty": 7,
        "UnitPrice": 56000,
    },
    {
        "LineID": 4,
        "OrderID": "O2024-0601",
        "ProductID": "P-VFD22",
        "Qty": 5,
        "UnitPrice": 45000,
    },
    {
        "LineID": 5,
        "OrderID": "O2024-0901",
        "ProductID": "P-IM55",
        "Qty": 4,
        "UnitPrice": 128000,
    },
    {
        "LineID": 6,
        "OrderID": "O2024-0901",
        "ProductID": "P-VFD22",
        "Qty": 6,
        "UnitPrice": 45000,
    },
    {
        "LineID": 7,
        "OrderID": "O2025-0401",
        "ProductID": "P-VFD7.5",
        "Qty": 20,
        "UnitPrice": 18000,
    },
    {
        "LineID": 8,
        "OrderID": "O2025-0301",
        "ProductID": "P-IM55",
        "Qty": 6,
        "UnitPrice": 128000,
    },
    {
        "LineID": 9,
        "OrderID": "O2024-0815",
        "ProductID": "P-IM55",
        "Qty": 2,
        "UnitPrice": 128000,
    },
    {
        "LineID": 10,
        "OrderID": "O2024-0815",
        "ProductID": "P-VFD7.5",
        "Qty": 10,
        "UnitPrice": 18000,
    },
    {
        "LineID": 11,
        "OrderID": "O2023-0510",
        "ProductID": "P-IM55",
        "Qty": 7,
        "UnitPrice": 128000,
    },
    {
        "LineID": 12,
        "OrderID": "O2023-0510",
        "ProductID": "P-VFD22",
        "Qty": 7,
        "UnitPrice": 45000,
    },
    {
        "LineID": 13,
        "OrderID": "O2023-1120",
        "ProductID": "P-IM15",
        "Qty": 10,
        "UnitPrice": 56000,
    },
    {
        "LineID": 14,
        "OrderID": "O2023-1120",
        "ProductID": "P-VFD7.5",
        "Qty": 10,
        "UnitPrice": 18000,
    },
    {
        "LineID": 15,
        "OrderID": "O2024-0315",
        "ProductID": "P-IM15",
        "Qty": 5,
        "UnitPrice": 56000,
    },
    {
        "LineID": 16,
        "OrderID": "O2024-0315",
        "ProductID": "P-VFD22",
        "Qty": 4,
        "UnitPrice": 45000,
    },
    {
        "LineID": 17,
        "OrderID": "O2024-1005",
        "ProductID": "P-IM55",
        "Qty": 2,
        "UnitPrice": 128000,
    },
    {
        "LineID": 18,
        "OrderID": "O2024-1005",
        "ProductID": "P-VFD7.5",
        "Qty": 5,
        "UnitPrice": 18000,
    },
]

# OPPORTUNITIES
opps = [
    {
        "OpportunityID": "OP2025-0001",
        "CustomerID": "CU002",
        "Name": "電網升級高壓變頻器",
        "Stage": "Negotiation",
        "Amount": 3500000,
        "Probability": 80,
        "CloseDate": "2025-06-30",
    },
    {
        "OpportunityID": "OP2025-0002",
        "CustomerID": "PC001",
        "Name": "塑膠廠能效改善",
        "Stage": "Negotiation",
        "Amount": 2000000,
        "Probability": 75,
        "CloseDate": "2025-09-01",
    },
    {
        "OpportunityID": "OP2025-0003",
        "CustomerID": "PC002",
        "Name": "EMS 系統整合",
        "Stage": "Lead",
        "Amount": 5000000,
        "Probability": 20,
        "CloseDate": "2025-12-31",
    },
    {
        "OpportunityID": "OP2025-0004",
        "CustomerID": "CU001",
        "Name": "廠房擴建馬達升級",
        "Stage": "Proposal",
        "Amount": 4200000,
        "Probability": 60,
        "CloseDate": "2025-07-15",
    },
    {
        "OpportunityID": "OP2025-0005",
        "CustomerID": "PC003",
        "Name": "AI 晶片散熱解決方案",
        "Stage": "Proposal",
        "Amount": 2800000,
        "Probability": 65,
        "CloseDate": "2025-08-15",
    },
]

# INVENTORY
inventory = [
    {
        "ProductID": "P-IM15",
        "CurrentStock": 50,
        "SafetyStock": 20,
        "LastReplenished": "2025-04-01",
    },
    {
        "ProductID": "P-VFD22",
        "CurrentStock": 70,
        "SafetyStock": 20,
        "LastReplenished": "2025-04-01",
    },
    {
        "ProductID": "P-IM55",
        "CurrentStock": 15,
        "SafetyStock": 5,
        "LastReplenished": "2025-04-10",
    },
]

wjsonl("contacts.jsonl", contacts)
wjsonl("customers.jsonl", customers)
wjsonl("products.jsonl", products)
wjsonl("orders.jsonl", orders)
wjsonl("order_lines.jsonl", order_lines)
wjsonl("opportunities.jsonl", opps)
wjsonl("inventory.jsonl", inventory)

schema = textwrap.dedent("""\
tables:
  Contacts:
    description: "Master table for contact personnel. Stores essential information for individuals associated with customers or internal departments."
    columns:
      ContactID:    {type: TEXT, pk: true}
      LastName:     {type: TEXT}
      FirstName:    {type: TEXT}
      Email:        {type: TEXT}
      Mobile:       {type: TEXT}
      Preferred:    {type: TEXT}
      Department:   {type: TEXT}
      Title:        {type: TEXT}
      Active:       {type: TEXT}
      Timezone:     {type: TEXT}

  Customers:
    description: "Central repository for all customer accounts, including active clients and prospective leads. Captures identifying, locational, and relationship details."
    columns:
      CustomerID:   {type: TEXT, pk: true}
      CompanyName:  {type: TEXT}
      UBN:          {type: TEXT}
      Type:         {type: TEXT}
      Address:      {type: TEXT}
      City:         {type: TEXT}
      Region:       {type: TEXT}
      PostalCode:   {type: TEXT}
      Country:      {type: TEXT}
      ContactID:    {type: TEXT}
      ContactName:  {type: TEXT}
      ContactTitle: {type: TEXT}
      Email:        {type: TEXT}
      Phone:        {type: TEXT}
      Fax:          {type: TEXT}
      RegisteredDate: {type: TEXT}
      Level:        {type: TEXT}
      Status:       {type: TEXT}
      VIPFlag:      {type: TEXT}

  Products:
    description: "Catalog of all products offered, including manufactured goods and resale items. Details product specifications, categorization, and pricing."
    columns:
      ProductID:    {type: TEXT, pk: true}
      ProductName:  {type: TEXT}
      Category:     {type: TEXT}
      Model:        {type: TEXT}
      Origin:       {type: TEXT}
      ListPrice:    {type: REAL}

  Orders:
    description: "Tracks customer sales orders from creation through fulfillment. Contains header-level information for each transaction."
    columns:
      OrderID:      {type: TEXT, pk: true}
      CustomerID:   {type: TEXT}
      OrderDate:    {type: TEXT}
      ShipDate:     {type: TEXT}
      Status:       {type: TEXT}
      TotalAmount:  {type: REAL}
      Currency:     {type: TEXT}
      Comments:     {type: TEXT}

  OrderLines:
    description: "Details individual line items within each customer order. Links products to orders and specifies quantities and agreed-upon unit prices."
    columns:
      LineID:       {type: INTEGER, pk: true}
      OrderID:      {type: TEXT}
      ProductID:    {type: TEXT}
      Qty:          {type: INTEGER}
      UnitPrice:    {type: REAL}

  Opportunities:
    description: "Manages potential sales deals and tracks their progression through the sales pipeline. Includes valuation, probability, and forecasted close dates."
    columns:
      OpportunityID: {type: TEXT, pk: true}
      CustomerID:   {type: TEXT}
      Name:         {type: TEXT}
      Stage:        {type: TEXT}
      Amount:       {type: REAL}
      Probability:  {type: INTEGER}
      CloseDate:    {type: TEXT}

  Inventory:
    description: "Monitors current stock levels, safety stock thresholds, and replenishment history for all products. Essential for supply chain management and order fulfillment."
    columns:
      ProductID:    {type: TEXT, pk: true}
      CurrentStock: {type: INTEGER}
      SafetyStock:  {type: INTEGER}
      LastReplenished: {type: TEXT}
""").strip()

(base_dir / "schema.yaml").write_text(schema, encoding="utf-8")

print("Sample CRM SQLite data prepared at", base_dir)
