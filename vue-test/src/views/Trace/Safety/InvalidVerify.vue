<template>
  <div>
    <div class="divHelp">
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <p>此页面可以一次性验证全部场景</p>
        <p>表格中第一列勾选场景，可以验证或重置所选场景</p>
        <br />
        <p>验证：点击验证按钮，将依次验证场景安全性，若判断为危险，则该场景标红显示</p>
        <p>重置：点击重置按钮即可重置验证结果</p>
        <p>全部验证结果：在表格右侧会有全部的验证信息结果</p>
        <el-button icon="el-icon-message-solid" circle slot="reference"></el-button>
      </el-popover>
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <div>
          <p>此页面可以一次性验证全部场景</p>
          <p>表格中第一列勾选场景，可以验证或重置所选场景</p>
          <br />
          <p>验证：点击验证按钮，将依次验证场景安全性，若判断为危险，则该场景标红显示</p>
          <p>重置：点击重置按钮即可重置验证结果</p>
          <p>全部验证结果：在表格右侧会有全部的验证信息结果</p>
        </div>
        <el-button type="text" slot="reference">操作提示</el-button>
      </el-popover>
    </div>
    <el-card style="width: 100%;height: 600px">
      <el-col :span="19">
        <div class="divForm">
          <span>选择场景进行验证</span>
          <el-button style="margin-left: 20px" type="primary" :disabled="buttonVerify" @click="verifyAll">验证</el-button>
          <el-button style="margin-left: 50px" type="primary" v-show="buttonReset" @click="handleReset">重置验证结果</el-button>
          <el-table
            ref="multipleTable"
            :data="tableData"
            :row-class-name="tableRowClassName"
            tooltip-effect="dark"
            style="width: 100%;margin-top: 20px"
            @selection-change="handleSelectionChange"
            border
            :header-cell-style="{ background: '#eef1f6', color: '#606266' }"
          >
            <el-table-column type="selection" width="40px"> </el-table-column>
            <el-table-column label="Id" width="50px" align="center">
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.invalid_id }}</span>
              </template>
            </el-table-column>
            <el-table-column label="名称" width="120px" align="center">
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.invalid_name }}</span>
              </template>
            </el-table-column>
            <el-table-column label="失效场景" width="640px" align="center">
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.invalid_content }}</span>
              </template>
            </el-table-column>
            <el-table-column label="验证结果" width="97px" align="center">
              <template slot-scope="scope">
                <span style="margin-left: 10px">{{ scope.row.invalid_verify }}</span>
              </template>
            </el-table-column>
            <!--        <el-table-column label="操作" align="center">-->
            <!--          <template slot-scope="scope">-->
            <!--            &lt;!&ndash;            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>&ndash;&gt;-->
            <!--            <el-button size="mini" type="primary" @click="handleVerify(scope.$index, scope.row)">验证</el-button>-->
            <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看完整验证信息</el-button>-->
            <!--          </template>-->
            <!--        </el-table-column>-->
          </el-table>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="page"
            :page-sizes="[1, 2, 4, 7, 10]"
            :page-size="limit"
            layout="total, sizes, prev, pager, next, jumper"
            background
            :total="total"
            style="margin-left: 30%;margin-top: 10px"
          >
          </el-pagination>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="divInfo" v-show="true">
          <el-card class="cardInfo">
            <p>总场景数：{{ total }}</p>
            <br />
            <p>已验证个数：{{ msg.numVerify }}</p>
            <p>未验证个数：{{ msg.numNoVerify }}</p>
            <br />
            <p>存在安全隐患数：{{ msg.numDanger }}</p>
          </el-card>
        </div>
      </el-col>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'InvalidVerify.vue',
  inject: ['reload'],
  data() {
    return {
      tableData: [],
      multipleSelection: [],
      limit: 7, //每页显示条数
      total: null, //trace总数
      page: 1, //第几页
      buttonReset: false, //重置按钮
      buttonVerify: true,
      infoReset: [], //需要重置的信息
      infoVerify: [],
      divInfoVisible: false,
      msg: {
        numVerify: 0,
        numNoVerify: 0,
        numDanger: 0,
        numSuccess: 0
      }
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    handleSelectionChange(val) {
      // this.multipleSelection = val
      console.log(val)
      this.infoReset = val
      this.infoVerify = val
      if (val.length > 0) {
        this.buttonReset = true
        this.buttonVerify = false
      } else {
        this.buttonReset = false
        this.buttonVerify = true
      }
    },
    handleReset() {
      this.$http
        .post('http://127.0.0.1:8000/api/reset_verify', this.infoReset)
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            this.pageList()
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/invalid_list')
        .then(response => {
          // console.log(response.data.trace_list)
          this.data = response.data.invalid_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    // 处理数据
    getList() {
      // es6过滤得到满足搜索条件的展示数据list
      // eslint-disable-next-line no-unused-vars
      // console.log({ test: this.search })
      // let list = this.data.filter((item, index) => item.invalid_content.includes(this.search))
      let list = this.data
      this.tableData = list.filter((item, index) => index < this.page * this.limit && index >= this.limit * (this.page - 1))
      this.total = list.length
      console.log(this.tableData)
      var tt = 0
      this.msg = {
        numVerify: 0,
        numNoVerify: 0,
        numDanger: 0,
        numSuccess: 0
      }
      while (tt < this.total) {
        if (this.tableData[tt].invalid_verify === 'null') {
          this.msg.numNoVerify++
        } else if (this.tableData[tt].invalid_verify === 'danger') {
          this.msg.numVerify++
          this.msg.numDanger++
        } else if (this.tableData[tt].invalid_verify === 'success') {
          this.msg.numSuccess++
          this.msg.numVerify++
        }
        tt++
      }
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
    // handleVerify(index, row) {
    //   console.log(index, row)
    //   this.$http
    //     .post('http://127.0.0.1:8000/api/verify_invalid', { invalid: row })
    //     .then(response => {
    //       console.log(response.data)
    //       if (response.data.error_code === 0) {
    //         this.pageList()
    //       }
    //     })
    //     .catch(function(error) {
    //       console.log(error)
    //     })
    // },
    handleShow(index, row) {
      console.log(index, row)
    },
    tableRowClassName({ row, rowIndex }) {
      // console.log(row.invalid_verify)
      if (row.invalid_verify === 'success') {
        return 'success-row'
      } else if (row.invalid_verify === 'danger') {
        return 'danger-row'
      }
      // if (rowIndex === 1) {
      //   return 'danger-row'
      // } else if (rowIndex === 2) {
      //   return 'success-row'
      // }
    },
    handleVerify(data, i) {
      if (i >= data.length) {
        // todo
        this.divInfoVisible = true
      } else {
        this.$http
          .post('http://127.0.0.1:8000/api/verify_invalid', { invalid: data[i] })
          .then(response => {
            console.log(response.data)
            if (response.data.error_code === 0) {
              this.pageList()
              i++
              // if (response.data.res === 'danger') {
              //   this.msg.numDanger++
              // } else if (response.data.res === 'success') {
              //   this.msg.numSuccess++
              // }
              this.handleVerify(data, i)
            }
          })
          .catch(function(error) {
            console.log(error)
          })
      }
    },
    verifyAll() {
      // todo: 计算不合理
      // this.msg.numVerify = this.infoVerify.length
      // this.msg.numNoVerify = this.total - this.msg.numVerify
      this.handleVerify(this.infoVerify, 0)
    }
  }
}
</script>

<style>
.el-table .warning-row {
  background: oldlace;
}
.el-table .danger-row {
  background: #f56c6c;
}
.el-table .success-row {
  background: #f0f9eb;
}
</style>
<style lang="scss" scoped>
.divInfo {
  //background: #ebb563;
  width: 100%;
  height: 100%;
  margin-top: 200px;
  margin-left: 25px;
  .cardInfo {
    //background: #ebb563;
    font-size: large;
  }
}
.divHelp {
  margin-left: 1100px;
  height: 40px;
  margin-top: -40px;
}
</style>
