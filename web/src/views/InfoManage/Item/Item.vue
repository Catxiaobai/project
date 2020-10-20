<template>
  <div id="item">
    <el-card class="tableTitle">
      <span style="font-size: 20px">当前系统共有{{ total }}个项目</span>
      <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <el-button size="20px" type="primary" style="margin-left: 400px" @click="handleAdd" icon="el-icon-plus">添加新项目</el-button>
      <el-button size="20px" type="primary" @click="handleLoad" icon="el-icon-download">一键导出</el-button>
      <!--    </el-card>-->
      <!--    &lt;!&ndash;    表格内容&ndash;&gt;-->
      <!--    <el-card class="traceTable" style="margin-top: 20px">-->
      <el-table :data="tableData" style="width: 100%;margin-top: 40px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
        <el-table-column label="序号" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.item_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="名称" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.item_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="项目介绍" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.item_introduction }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="handleOpen(scope.$index, scope.row)">打开</el-button>
            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>
            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--    </el-card>-->
      <!--    &lt;!&ndash;    分页显示&ndash;&gt;-->
      <!--    <el-card class="tablePage" style="margin-top: 20px">-->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 2, 5, 7, 10]"
        :page-size="limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-left: 30%;margin-top: 30px"
      >
      </el-pagination>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      dialogShowItem: false, //查看项目信息弹窗
      dialogAddItem: false, //添加新项目弹窗
      dialogEditItem: false, //编辑项目
      tableData: [], //项目表
      showItem: {} //查看项目
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/item_list')
        .then(response => {
          // console.log(response.data.item_list)
          this.data = response.data.item_list
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
      // console.log({ test: this.search })
      let list = this.data.filter((item, index) => item.item_introduction.includes(this.search))
      // let list = this.data
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
    handleOpen(index, row) {
      // console.log(row)
      this.bus.$emit('itemInfo', row)
    },
    handleAdd(index, row) {
      console.log(index, row)
    },
    handleLoad(index, row) {
      console.log(index, row)
    },
    handleShow(index, row) {
      console.log(index, row)
    },
    handleDelete(index, row) {
      console.log(index, row)
    },
    handleEdit(index, row) {
      console.log(index, row)
    }
  }
}
</script>

<style lang="scss" scoped>
.tableTitle {
  height: 634px;
  overflow-y: scroll;
}
</style>
