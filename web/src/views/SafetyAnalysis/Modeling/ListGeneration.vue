<template>
  <div id="modelList">
    <el-card>
      <download-excel :data="tableData" :fields="json_fields" name="output.xls">
        <el-button type="primary" style="margin-bottom: 20px;margin-left: 90%">导出</el-button>
      </download-excel>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column prop="id" label="序号" width="80" align="center"></el-table-column>
          <el-table-column prop="model_name" label="模型名称" align="center"></el-table-column>
          <el-table-column prop="element" label="场景类别" align="center"></el-table-column>
          <el-table-column prop="name" label="场景名称" align="center"></el-table-column>
          <el-table-column prop="type2" label="场景所属" align="center"></el-table-column>
          <!--          <el-table-column prop="describe" label="场景描述" width="180"> </el-table-column>-->
          <!--          <el-table-column prop="content" label="场景内容"> </el-table-column>-->
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
  </div>
</template>

<script>
export default {
  name: 'ModelList.vue',
  data() {
    return {
      json_fields: {
        序号: 'id',
        模型名称: 'model_name',
        场景类别: 'element',
        场景名称: 'name',
        场景所属: 'type2'
      },
      tableData: [],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '', //搜索框
      itemInfo: ''
    }
  },
  created() {
    this.getItemInfo()
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
        .post(this.Global_Api + '/api/model_list', this.itemInfo)
        .then(response => {
          // console.log(response.data.analysis_list)
          this.data = response.data.model_list
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
      let list = this.data.filter((item, index) => item.name.includes(this.search))
      // let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('模型列表', this.itemInfo)
    }
  }
}
</script>

<style scoped></style>
