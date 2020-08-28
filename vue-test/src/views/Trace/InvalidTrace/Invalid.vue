<template>
  <div>
    <el-row :gutter="20">
      <el-card class="box-card">
        <el-table :data="tableData" style="width: 100%">
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
                <el-form-item label="细节描述">
                  <span>{{ props.row.description }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column label="场景 ID" prop="id"> </el-table-column>
          <el-table-column label="名称" prop="name"> </el-table-column>
          <!--        <el-table-column label="描述" prop="desc"> </el-table-column>-->
        </el-table>
        <div style="margin-top: 20px;">
          <!--        <el-button type="primary" round @click="gotolink">-->
          <!--          生成模型-->
          <!--        </el-button>-->
        </div>
      </el-card>
    </el-row>
    <!--    <el-pagination background layout="prev, pager, next" :total="1000"> </el-pagination>-->
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
export default {
  data() {
    return {
      tableData: [
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
        }
      ],
      fileList: [
        {
          name: 'trace1-10.txt',
          url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'
        }
      ]
    }
  },
  methods: {
    gotolink() {
      this.$router.replace('/page2')
    },
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log(file)
    },
    handleExceed(files, fileList) {
      this.$message.warning(`当前限制选择 3 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`)
    },
    // eslint-disable-next-line no-unused-vars
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    }
  }
}
</script>
<style lang="scss" scoped></style>
