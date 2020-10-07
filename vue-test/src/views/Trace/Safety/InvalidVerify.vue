<template>
  <div>
    <el-card style="width: 100%;height: 600px">
      <span>选择场景进行验证</span>
      <el-table
        ref="multipleTable"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%;margin-top: 20px"
        @selection-change="handleSelectionChange"
        stripe
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
        <el-table-column label="失效场景" width="650px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.invalid_content }}</span>
          </template>
        </el-table-column>
        <el-table-column label="验证结果" width="100px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.invalid_verify }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>-->
            <el-button size="mini" type="primary" @click="handleVerify(scope.$index, scope.row)">验证</el-button>
            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看完整验证信息</el-button>
          </template>
        </el-table-column>
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
      <el-button style="margin-top: 10px;margin-left: 50px" type="primary" v-show="buttonReset" @click="handleReset">重置</el-button>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'InvalidVerify.vue',
  data() {
    return {
      tableData: '',
      multipleSelection: [],
      limit: 7, //每页显示条数
      total: null, //trace总数
      page: 1, //第几页
      buttonReset: false, //重置按钮
      infoReset: [] //需要重置的信息
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
      if (val.length > 0) this.buttonReset = true
      else this.buttonReset = false
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
    handleVerify(index, row) {
      console.log(index, row)
      this.$http
        .post('http://127.0.0.1:8000/api/verify_invalid', { invalid: row })
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
    handleShow(index, row) {
      console.log(index, row)
    }
  }
}
</script>

<style scoped></style>
