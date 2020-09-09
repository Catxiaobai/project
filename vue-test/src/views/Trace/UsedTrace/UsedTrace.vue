<template>
  <div>
    <!--    标题-->
    <el-card class="tableTitle">
      <span>当前项目共有{{ total }}条使用场景</span>
      <el-button size="20px" type="primary" style="margin-left: 50px" @click="handleAdd()">添加新场景</el-button>
      <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left:50px; width: 300px" />
    </el-card>
    <!--    表格内容-->
    <el-card class="traceTable" style="margin-top: 20px">
      <el-table :data="tableData" style="width: 100%;" stripe border>
        <el-table-column label="Id" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.trace_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="名称" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.trace_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="描述" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.trace_describe }}</span>
          </template>
        </el-table-column>
        <el-table-column label="动作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>
            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!--    分页显示-->
    <el-card class="tablePage" style="margin-top: 20px">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 2, 4, 8]"
        :page-size="limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-left: 35%"
      >
      </el-pagination>
    </el-card>
    <!--    某一trace弹窗-->
    <el-dialog title="暂定以弹窗形式呈现" :visible.sync="dialogShowTrace" width="30%" class="showTraceDialog">
      <span style="display: block">场景名称：{{ showTrace.trace_name }}</span>
      <span style="margin-top: 10px;display: block">场景内容：{{ showTrace.trace_content }}</span>
      <span style="margin-top: 10px;display: block">场景描述：{{ showTrace.trace_details }}</span>
      <span slot="footer" class="dialog-footer">
        <!--        <el-button @click="dialogShowTrace = false">取 消</el-button>-->
        <el-button type="primary" @click="dialogShowTrace = false">OK</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'UsedTrace.vue',
  data() {
    return {
      limit: 2, //每页显示条数
      total: null, //trace总数
      page: 1, //第几页
      search: '', //todo: 搜索框
      dialogShowTrace: false, //查看trace弹窗
      tableData: [], //trace表
      showTrace: {}
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/trace_list')
        .then(response => {
          console.log(response.data.trace_list)
          this.data = response.data.trace_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    // 处理数据
    getList() {
      // es6过滤得到满足搜索条件的展示数据list
      // eslint-disable-next-line no-unused-vars
      // let list = this.data.filter((item, index) => item.name.includes(this.searchData))
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
    handleShow(index, row) {
      this.dialogShowTrace = true
      console.log(index, row)
      this.showTrace = row
      // this.showTrace.showId = row.trace_id
      // this.showTrace.showContent = row.trace_content
      // this.showTrace.showDescribe = row.trace_describe
      // this.showTrace.showDetails = row.trace_details
      // this.showTrace.showName = row.trace_name
    },
    handleEdit(index, row) {
      console.log(index, row)
    },
    handleDelete(index, row) {
      console.log(index, row)
    },
    handleAdd(val) {
      console.log(val)
    }
  }
}
</script>

<style lang="scss" scoped></style>
