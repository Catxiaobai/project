<template>
  <div>
    <el-row :gutter="20">
      <el-card class="box-card">
        <el-table :data="list" style="width: 100%">
          <el-table-column type="expand">
            <template slot-scope="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="ID">
                  <span>{{ props.row.id }}</span>
                </el-form-item>
                <el-form-item label="场景名称">
                  <span>{{ props.row.name }}</span>
                </el-form-item>
                <el-form-item label="具体内容">
                  <span>{{ props.row.category }}</span>
                </el-form-item>
                <el-form-item label="文字描述">
                  <span>{{ props.row.description }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column label="场景 ID" prop="id"> </el-table-column>
          <el-table-column label="名称" prop="name"> </el-table-column>
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          style="margin-top: 20px;margin-left: 25%"
          :current-page="page"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </el-card>
    </el-row>
  </div>
</template>

<style>
.demo-table-expand {
  font-size: 0;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 90%;
}
</style>

<script>
var listJson = {
  list: [
    {
      id: '1',
      name: '场景1',
      category:
        'source:S1:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S2:输入密码页\n' +
        'source:S2:输入密码页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S3:初始页面\n',
      description: '用户插卡，ATM机从初始页面变为输入密码页,并显示要求用户输入密码信息，用户选择取消交易，ATM机显示取消操作信息并退出卡片返回初始页面。'
    },
    {
      id: '2',
      name: '场景2',
      category:
        'source:S4:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S5:输入密码页\n' +
        'source:S5:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:null\n' +
        'action:Write("Verify password timeout"),return_card\n' +
        'target:S6:初始页面\n',
      description: '用户插卡，ATM机从初始页面变为输入密码页,并显示要求用户输入密码信息，用户输入密码，ATM显示验证密码超时信息，并退出卡片返回初始页面'
    },
    {
      id: '3',
      name: '场景3',
      category:
        'source:S7:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S8:输入密码页\n' +
        'source:S8:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S9:输入密码页\n' +
        'source:S9:输入密码页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S10:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户选择了取消交易，ATM机显示取消操作信息并退出卡片返回初始页面。'
    },
    {
      id: '4',
      name: '场景4',
      category:
        'source:S11:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S12:输入密码页\n' +
        'source:S12:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S13:输入密码页\n' +
        'source:S13:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=1\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S14:输入密码页\n' +
        'source:S14:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=2\n' +
        'action=Write("Wrong Pin,Ejecting Card"),attempts=attempts+1\n' +
        'target:S15:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户在秒时重新输入了密码,ATM机显示密码错误次数超限页，并退出卡片并从提示密码错误次数超限页返回初始页面。'
    },
    {
      id: '5',
      name: '场景5',
      category:
        'source:S16:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S17:输入密码页\n' +
        'source:S17:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=0\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S18:用户选择页\n' +
        'source:S18:用户选择页\n' +
        'event:Withdrawal()\n' +
        'condition:null\n' +
        'action:Write("Enter amount")\n' +
        'target:S19:输入金额页\n' +
        'source:S19:输入金额页\n' +
        'event:Enter_amount(w)\n' +
        'condition:w<=B\n' +
        'action:Give_money,B=B-w,Write("your balance",B)\n' +
        'target:S20:显示余额页\n' +
        'source:S20:显示余额页\n' +
        'event:null\n' +
        'condition:null\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel")\n' +
        'target:S21:用户选择页\n' +
        'source:S21:用户选择页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S22:初始页面\n',
      description:
        '用户插卡,ATM机从初始页面变为输入密码页,并显示要求用户输入密码信息，用户输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面。用户选择取款操作，ATM机显示输入金额页请求用户输入金额,并输入金额，ATM机吐出金额并跳到显示余额页，从显示余额页返回用户选择页，用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面。 '
    },
    {
      id: '6',
      name: '场景6',
      category:
        'source:S38:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S39:输入密码页\n' +
        'source:S40:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=0\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S41:用户选择页\n' +
        'source:S41:用户选择页\n' +
        'event:Withdrawal()\n' +
        'condition:null\n' +
        'action:Write("Enter amount")\n' +
        'target:S42:输入金额页\n' +
        'source:S42:输入金额页\n' +
        'event:Enter_amount(w)\n' +
        'condition:w>B\n' +
        'action:Write("Out balance")\n' +
        'target:S43:余额不足页\n' +
        'source:S43:余额不足页\n' +
        'event:null\n' +
        'condition:null\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel")\n' +
        'target:S44:用户选择页\n' +
        'source:S44:用户选择页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S45:初始页面\n',
      description:
        '用户插卡,ATM机从初始页面变为输入密码页,并显示要求用户输入密码信息;用户输入密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面,用户选择取款操作，ATM机显示输入金额页请求用户输入金额,用户输入金额，ATM显示余额不足,从显示余额不足页返回用户选择页；用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面'
    },
    {
      id: '7',
      name: '场景7',
      category:
        'source:S46:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S47:输入密码页\n' +
        'source:S47:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S48:输入密码页\n' +
        'source:S48:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=1\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S49: 输入密码页\n' +
        'source:S49:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=2\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S50: 用户选择页\n' +
        'source:S50:用户选择页\n' +
        'event:Withdrawal()\n' +
        'condition:null\n' +
        'action:Write("Enter amount")\n' +
        'target:S51:输入金额页\n' +
        'source:S51:输入金额页\n' +
        'event:Enter_amount(w)\n' +
        'condition:w<=B\n' +
        'action:Give_money,B=B-w,Write("your balance",B)\n' +
        'target:S52:显示余额页\n' +
        'source:S52:显示余额页\n' +
        'event:Return()\n' +
        'condition:null\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel")\n' +
        'target:S53:用户选择页\n' +
        'source:S53:用户选择页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S54:初始页面\n',
      description:
        '用户插卡,ATM机从初始页面变为输入密码页,并显示要求用户输入密码信息; 用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户输入密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面,用户选择取款操作，ATM机显示输入金额页请求用户输入金额,用户输入金额，ATM机吐出金额并跳到显示余额页，从显示余额页返回用户选择页；用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面。'
    },
    {
      id: '8',
      name: '场景8',
      category:
        'source:S72:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S73:输入密码页\n' +
        'source:S73:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S74:输入密码页\n' +
        'source:S74:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=1\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S75:输入密码页\n' +
        'source:S75:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=2\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S76:用户选择页\n' +
        'source:S76:用户选择页\n' +
        'event:Withdrawal()\n' +
        'condition:null\n' +
        'action:Write("Enter amount")\n' +
        'target:S77:输入金额页\n' +
        'source:S77:输入金额页\n' +
        'event:Enter_amount(w)\n' +
        'condition:w<=B\n' +
        'action:Give_money,B=B-w,Write("your balance",B)\n' +
        'target:S78:显示余额页\n' +
        'source:S78:显示余额页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S79:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面。用户选择取款操作，ATM机显示输入金额页请求用户输入金额,并输入金额，ATM机吐出金额并跳到显示余额页，从显示余额页返回用户选择页，用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面。 '
    },
    {
      id: '9',
      name: '场景9',
      category:
        'source:S80:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S81:输入密码页\n' +
        'source:S81:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=0\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S82:用户选择页\n' +
        'source:S82:用户选择页\n' +
        'event:GetBalance()\n' +
        'condition:null\n' +
        'action:Write("your balance",B)\n' +
        'target:S83:显示余额页\n' +
        'source:S83:显示余额页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S84:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面。用户选择取款操作,并输入金额，ATM机吐出金额并跳到显示余额页，ATM机退出卡片并从显示余额页返回初始页面。 '
    },
    {
      id: '10',
      name: '场景10',
      category:
        'source:S85:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S86:输入密码页\n' +
        'source:S86:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S87:输入密码页\n' +
        'source:S87:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=1\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S88:用户选择页\n' +
        'source:S88:用户选择页\n' +
        'event:GetBalance()\n' +
        'condition:null\n' +
        'action:Write("your balance",B)\n' +
        'target:S89:显示余额页\n' +
        'source:S89:显示余额页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S90:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面,用户选择取款操作，用户选择取款操作,并输入金额，ATM机吐出金额并跳到显示余额页，ATM机退出卡片并从显示余额页返回初始页面。'
    },
    {
      id: '11',
      name: '场景11',
      category:
        'source:S91:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S92:输入密码页\n' +
        'source:S92:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S93:输入密码页\n' +
        'source:S93:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=1\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S94:输入密码页\n' +
        'source:S94:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=2\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S95:用户选择页\n' +
        'source:S95:用户选择页\n' +
        'event:GetBalance()\n' +
        'condition:null\n' +
        'action:Write("your balance",B)\n' +
        'target:S96:显示余额页\n' +
        'source:S96:显示余额页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S97:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面,用户选择查询余额操作，ATM机跳到显示余额页，ATM机退出卡片并从显示余额页返回初始页面。'
    },
    {
      id: '12',
      name: '场景12',
      category:
        'source:S98:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S99:输入密码页\n' +
        'source:S99:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=0\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S100:用户选择页\n' +
        'source:S100:用户选择页\n' +
        'event:GetBalance()\n' +
        'condition:null\n' +
        'action:Write("your balance",B)\n' +
        'target:S101:显示余额页\n' +
        'source:S101:显示余额页\n' +
        'event:Return()\n' +
        'condition:null\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel")\n' +
        'target:S102:用户选择页\n' +
        'source:S102:用户选择页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S103:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面。用户选择查询余额操作，ATM机跳到显示余额页；用户选择取消操作，ATM机跳到用户选择页，用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面。 '
    },
    {
      id: '13',
      name: '场景13',
      category:
        'source:S104:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S105:输入密码页\n' +
        'source:S105:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S106:输入密码页\n' +
        'source:S106:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=1\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S107:用户选择页\n' +
        'source:S107:用户选择页\n' +
        'event:GetBalance()\n' +
        'condition:null\n' +
        'action:Write("your balance",B)\n' +
        'target:S108:显示余额页\n' +
        'source:S108:显示余额页\n' +
        'event:Return()\n' +
        'condition:null\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel")\n' +
        'target:S109:用户选择页\n' +
        'source:S109:用户选择页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S110:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面。用户选择查询余额操作，ATM机跳到显示余额页；用户选择取消操作，ATM机跳到用户选择页，用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面。 '
    },
    {
      id: '14',
      name: '场景14',
      category:
        'source:S111:初始页面\n' +
        'event:Card(pin,B)\n' +
        'condition:null\n' +
        'action:Write("Enter Pin"),attempts=0\n' +
        'target:S112:输入密码页\n' +
        'source:S112:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=0\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S113:输入密码页\n' +
        'source:S113:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p!=pin,attempts=1\n' +
        'action:Write("Wrong Pin,ReEnter"),attempts=attempts+1\n' +
        'target:S114:输入密码页\n' +
        'source:S114:输入密码页\n' +
        'event:Enter_pin(p)\n' +
        'condition:p=pin,attempts=2\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1\n' +
        'target:S115:用户选择页\n' +
        'source:S115:用户选择页\n' +
        'event:GetBalance()\n' +
        'condition:null\n' +
        'action:Write("your balance",B)\n' +
        'target:S116:显示余额页\n' +
        'source:S116:显示余额页\n' +
        'event:Return()\n' +
        'condition:null\n' +
        'action:Write("Select Withdrawal/GetBalance/Cancel")\n' +
        'target:S117:用户选择页\n' +
        'source:S117:用户选择页\n' +
        'event:Cancel()\n' +
        'condition:null\n' +
        'action:Write("Canceling"),return_card\n' +
        'target:S118:初始页面\n',
      description:
        '用户插卡，ATM机从初始页面变为输入密码页, 并显示要求用户输入密码信息；用户输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机显示密码错误信息,并从提示密码错误页返回输入密码页。用户重新输入了密码，ATM机跳转到显示包括取款、查询余额、取消等操作的用户选择页面。用户选择查询余额操作，ATM机跳到显示余额页；用户选择取消操作，ATM机跳到用户选择页，用户选择取消操作，ATM机退出卡片并从用户选择页返回初始页面。 '
    }
  ]
}
export default {
  data() {
    return {
      list: [],
      data: [],
      limit: 5,
      total: null,
      page: 1,
      searchData: ''
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.data = listJson.list
      this.getList()
    },
    // 处理数据
    getList() {
      // es6过滤得到满足搜索条件的展示数据list
      // eslint-disable-next-line no-unused-vars
      let list = this.data.filter((item, index) => item.name.includes(this.searchData))
      this.list = list.filter((item, index) => index < this.page * this.limit && index >= this.limit * (this.page - 1))
      this.total = list.length
    },
    // 当每页数量改变
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.limit = val
      this.getList()
    },
    // 当当前页改变
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.getList()
    },
    search() {
      this.page = 1
      this.getList()
    }
  }
}
</script>
<style lang="scss" scoped>
/** iframe样式 */
#iframeContain {
  width: 100%;
  height: 600px;
}
</style>
