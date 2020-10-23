<template>
  <div id="analysisBase">
    <el-card style="height: 634px">
      <!--      <el-button @click="resetDateFilter">清除分组过滤器</el-button>-->

      <span style="font-size: 20px">当前系统共有{{ total }}个通用分析规则</span>
      <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <el-button size="20px" type="primary" style="margin-left: 240px" @click="handleAdd" icon="el-icon-plus">添加新规则</el-button>
      <el-button size="20px" type="primary" @click="handleLoad" icon="el-icon-upload2">导入</el-button>
      <el-button size="20px" type="primary" @click="handleLoad" icon="el-icon-download">保存</el-button>
      <el-table ref="filterTable" :data="tableData" style="width: 100%">
        <el-table-column label="序号" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.id }}</span>
          </template>
        </el-table-column>
        <!--        <el-table-column label="名称" width="180px" align="center">-->
        <!--          <template slot-scope="scope">-->
        <!--            <span style="margin-left: 10px">{{ scope.row.name }}</span>-->
        <!--          </template>-->
        <!--        </el-table-column>-->
        <el-table-column
          label="类别"
          width="180"
          :filters="[
            { text: '外部接口', value: '外部接口' },
            { text: '功能处理', value: '功能处理' },
            { text: '功能层次', value: '功能层次' },
            { text: '状态迁移', value: '状态迁移' },
            { text: '其他', value: '其他' }
          ]"
          :filter-method="filterTag"
          filter-placement="bottom-end"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.type }}</span>
          </template>
          <!--          <template slot-scope="scope">-->
          <!--            <el-tag :type="scope.row.type === '属性一' ? 'primary' : 'success'" disable-transitions>{{ scope.row.type }}</el-tag>-->
          <!--          </template>-->
        </el-table-column>
        <el-table-column label="规则描述" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.content }}</span>
          </template>
        </el-table-column>
        <!--        <el-table-column-->
        <!--          prop="group"-->
        <!--          label="分组"-->
        <!--          sortable-->
        <!--          width="180"-->
        <!--          column-key="group"-->
        <!--          :filters="[-->
        <!--            { text: '外部接口', value: '外部接口' },-->
        <!--            { text: '功能处理', value: '功能处理' },-->
        <!--            { text: '功能层次', value: '功能层次' },-->
        <!--            { text: '状态迁移', value: '状态迁移' },-->
        <!--            { text: '其他', value: '其他' }-->
        <!--          ]"-->
        <!--          :filter-method="filterHandler"-->
        <!--        >-->
        <!--        </el-table-column>-->

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
  name: 'AnalysisBase.vue',
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: [
        {
          id: '1',
          name: '分析规则一',
          content: '不知道是什么东西',
          group: '外部接口',
          type: '外部接口'
        },
        {
          id: '2',
          name: '分析规则二',
          content: '不知道是什么东西',
          group: '功能处理',
          type: '功能处理'
        },
        {
          id: '3',
          name: '分析规则三',
          content: '不知道是什么东西',
          group: '功能层次',
          type: '功能层次'
        },
        {
          id: '4',
          name: '分析规则四',
          content: '不知道是什么东西',
          group: '状态迁移',
          type: '状态迁移'
        },
        {
          id: '5',
          name: '分析规则五',
          content: '不知道是什么东西',
          group: '其他',
          type: '其他'
        },
        {
          id: '6',
          name: '分析规则六',
          content: '不知道是什么东西',
          group: '其他',
          type: '其他'
        },
        {
          id: '7',
          name: '分析规则七',
          content: '不知道是什么东西',
          group: '外部接口',
          type: '外部接口'
        }
      ]
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
    filterHandler(value, row, column) {
      const property = column['property']
      return row[property] === value
    },
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/analysis_rule_list')
        .then(response => {
          // console.log(response.data.item_list)
          this.data = response.data.analysis_list
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

<style scoped>
#analysisBase {
  height: 620px;
}
</style>
