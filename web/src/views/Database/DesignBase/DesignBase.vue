<template>
  <div id="designBase">
    <el-card style="height: 634px">
      <!--      <el-button @click="resetDateFilter">清除分组过滤器</el-button>-->

      <span style="font-size: 20px">当前系统共有{{ total }}个通用设计准则</span>
      <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <el-button size="20px" type="primary" style="margin-left: 240px" @click="handleAdd" icon="el-icon-plus">添加新准则</el-button>
      <el-button size="20px" type="primary" @click="handleUpload" icon="el-icon-upload2">导入</el-button>
      <el-button size="20px" type="primary" @click="handleDownload" icon="el-icon-download">保存</el-button>
      <el-table ref="filterTable" :data="tableData" style="width: 100%">
        <el-table-column label="序号" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="要素"
          width="180"
          :filters="[
            { text: '接口相关', value: '接口相关' },
            { text: '功能处理', value: '功能处理' },
            { text: '功能划分', value: '功能划分' },
            { text: '状态迁移', value: '状态迁移' },
            { text: '其他', value: '其他' }
          ]"
          :filter-method="filterGroup"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.group }}</span>
          </template>
          <!--          <template slot-scope="scope">-->
          <!--            <el-tag :type="scope.row.type === '属性一' ? 'primary' : 'success'" disable-transitions>{{ scope.row.type }}</el-tag>-->
          <!--          </template>-->
        </el-table-column>
        <el-table-column label="类别" width="180">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === '硬件相关' ? 'primary' : 'success'" disable-transitions>{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <!--        <el-table-column label="名称" width="180px" align="center">-->
        <!--          <template slot-scope="scope">-->
        <!--            <span style="margin-left: 10px">{{ scope.row.name }}</span>-->
        <!--          </template>-->
        <!--        </el-table-column>-->
        <el-table-column label="准则描述" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.content }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <!--            <el-button size="mini" type="success" @click="handleOpen(scope.$index, scope.row)">打开</el-button>-->
            <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>-->
            <el-button size="mini" type="success" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
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
  name: 'DesignBase.vue',
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: []
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    resetDateFilter() {
      this.$refs.filterTable.clearFilter('group')
    },
    clearFilter() {
      this.$refs.filterTable.clearFilter()
    },
    formatter(row, column) {
      return row.name
    },
    filterTag(value, row) {
      return row.type === value
    },
    filterGroup(value, row) {
      // console.log(value, row)
      return row.group === value
    },
    filterHandler(value, row) {
      // const property = column['property']
      console.log(value, row)
      return row.type === value
    },
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/design_criteria_list')
        .then(response => {
          // console.log(response.data.design_list)
          this.data = response.data.design_list
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
      let list = this.data.filter((item, index) => item.type.includes(this.search))
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
    }
  }
}
</script>

<style scoped></style>
