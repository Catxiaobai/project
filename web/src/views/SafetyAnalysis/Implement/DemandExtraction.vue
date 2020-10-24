<template>
  <div id="demandExtraction">
    <el-card>
      <div style="margin-top: 20px">
        <div id="table">
          <el-table :data="tableData" border style="width: 100%">
            <el-table-column prop="id" label="序号" width="80" align="center"> </el-table-column>
            <el-table-column prop="describe" label="失效描述" width="180" align="center"> </el-table-column>
            <el-table-column prop="improve" label="改进措施" width="180" align="center"> </el-table-column>
            <el-table-column prop="demand" label="软件安全性需求" align="center">
              <template slot-scope="scope">
                <el-input class="tableCell" type="textarea" autosize v-model="scope.row.demand" @change="saveData(scope.row)"> </el-input>
              </template>
            </el-table-column>
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
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'DemandExtraction.vue',
  data() {
    return {
      tableData: [],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '' //搜索框
    }
  },
  created() {
    this.pageList()
  },
  methods: {
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
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/demand_list')
        .then(response => {
          console.log(response.data.demand_list)
          this.data = response.data.demand_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    getList() {
      // 处理数据，根据表格中name字段来筛选
      let list = this.data.filter((item, index) => item.describe.includes(this.search))
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
    },
    saveData(val) {
      console.log(val)
      this.$http
        .post('http://127.0.0.1:8000/api/edit_demand', val)
        .then(response => {
          if (response.data.error_code === 0) {
            this.pageList()
          } else {
            console.log(response.data)
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
<style lang="scss">
.tableCell {
  .el-textarea__inner {
    border: none;
    resize: none;
  }
}
</style>
