<template>
  <div id="generalCriteria">
    <el-card>
      <div id="actionButton" style="margin-left: 50px">
        <el-popconfirm icon="el-icon-loading" iconColor="blue" title="是否将所选规则加入此项目设计准则库？" @onConfirm="handleSelectCommit">
          <el-button type="primary" :disabled="disabled.select" slot="reference">选择加入此项目</el-button>
        </el-popconfirm>
      </div>
      <div id="search" style="margin-left:75%;margin-bottom: 20px;margin-top: -40px">
        <el-input v-model="search" placeholder="按类别搜索" style="width: 300px" @input="pageList" />
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection" @filter-change="handleFilterChange">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="id" label="序号" width="180"> </el-table-column>
          <el-table-column prop="element" label="要素" width="180" :filters="filterData" column-key="element"> </el-table-column>
          <el-table-column prop="type" label="类别" width="180"> </el-table-column>
          <el-table-column prop="describe" label="描述"> </el-table-column>
        </el-table>
      </div>
      <div id="page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[1, 2, 5, 7, 10]"
          :page-size="pagination.limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          style="margin-left: 30%;margin-top: 20px"
        >
        </el-pagination>
      </div>
    </el-card>
    <div id="select">
      <el-dialog title="选择" :visible.sync="visible.selectDialog">
        <span>是否选择以下 {{ selectData.length }} 条设计准则加入该项目准则库</span>
        <el-card style="margin-top: 10px">
          <el-table :data="selectData" border>
            <el-table-column property="id" label="序号" width="50"></el-table-column>
            <el-table-column property="type" label="类别" width="150"></el-table-column>
            <el-table-column property="describe" label="名称"></el-table-column>
          </el-table>
        </el-card>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.deleteDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleSelectCommit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GeneralCriteria.vue',
  data() {
    return {
      tableData: [],
      itemInfo: '',
      filterData: [
        { text: '接口相关设计', value: '接口相关设计' },
        { text: '功能处理相关设计', value: '功能处理相关设计' },
        { text: '功能划分相关设计', value: '功能划分相关设计' },
        { text: '状态迁移相关设计', value: '状态迁移相关设计' },
        { text: '其他设计', value: '其他设计' }
      ],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '', //搜索框
      visible: {
        selectDialog: false
      },
      disabled: {
        select: true
      },
      selectData: []
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get(this.Global_Api + '/api/design_criteria_list')
        .then(response => {
          // console.log(response.data.analysis_list)
          this.data = response.data.design_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    getList() {
      // 处理数据，根据表格中type字段来筛选
      let list = this.data.filter((item, index) => item.type.includes(this.search))
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
    },
    filterElement(value, row) {
      console.log(value, row)
      return row.element === value
    },
    handleFilterChange(value) {
      console.log(value)
      if (value['element']) {
        this.filterSearch = value['element']
        let list = this.data.filter((item, index) => item.element.includes(this.filterSearch))
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
      if (value['type']) {
        this.filterSearch = value['type']
        let list = this.data.filter((item, index) => item.type.includes(this.filterSearch))
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
    },
    handleSizeChange(val) {
      // 当每页数量改变
      console.log(`每页 ${val} 条`)
      this.pagination.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      // 当当前页改变
      console.log(`当前页: ${val}`)
      this.pagination.page = val
      this.getList()
    },
    handleSelection(val) {
      if (val.length === 0) {
        this.disabled.select = true
      } else {
        this.disabled.select = false
        this.selectData = val
      }
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log(this.itemInfo)
    },
    handleSelectCommit() {
      this.getItemInfo()
      this.visible.selectDialog = false
      this.$http
        .post(this.Global_Api + '/api/add_design', { selectData: this.selectData, item: this.itemInfo, belong: '通用' })
        .then(response => {
          if (response.data.error_code === 0) {
            alert('添加成功')
            this.pageList()
            this.visible.deleteDialog = false
          } else {
            console.log(response.data)
            alert(response.data.error_message)
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped></style>
