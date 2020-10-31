<template>
  <div id="modelList">
    <el-card>
      <el-button type="primary" style="margin-bottom: 20px;margin-left: 90%">导出</el-button>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%">
          <el-table-column prop="id" label="序号" width="180"> </el-table-column>
          <el-table-column prop="model_name" label="模型名称" width="180"> </el-table-column>
          <el-table-column prop="element" label="场景要素" width="180"> </el-table-column>
          <el-table-column prop="name" label="场景名称" width="180"> </el-table-column>
          <el-table-column prop="type" label="场景类型"> </el-table-column>
          <el-table-column prop="model_type" label="模型类型" width="180" :filters="filterData" :filter-method="filterType">
            <!--todo: 筛选功能存在bug-->
          </el-table-column>
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
      tableData: [
        {
          id: 1,
          model_name: 'ATM系统',
          model_type: '状态机',
          element: '状态迁移',
          name: '取款',
          type: '综合场景'
        },
        {
          id: 2,
          model_name: 'ATM系统',
          model_type: '状态机',
          element: '状态迁移',
          name: '存款',
          type: '综合场景'
        },
        {
          id: 3,
          model_name: 'ATM系统',
          model_type: '状态机',
          element: '状态迁移',
          name: '输密码',
          type: '综合场景'
        }
      ],
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      filterData: [
        { text: '状态机', value: '状态机' },
        { text: '时序图', value: '时序图' },
        { text: '活动图', value: '活动图' },
        { text: '顺序图', value: '顺序图' }
      ]
    }
  },
  created() {
    this.pagination.total = this.tableData.length
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
    }
  }
}
</script>

<style scoped></style>
