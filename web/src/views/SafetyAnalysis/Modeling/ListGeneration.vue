<template>
  <div id="modelList">
    <el-card>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection">
          <el-table-column prop="name" label="模型名称" width="180"> </el-table-column>
          <el-table-column prop="type" label="模型类型" width="180" :filters="filterData" :filter-method="filterType">
            <!--todo: 筛选功能存在bug-->
          </el-table-column>
          <el-table-column prop="factor" label="场景要素" width="180"> </el-table-column>
          <el-table-column prop="describe" label="场景名称" width="180"> </el-table-column>
          <el-table-column prop="remark" label="备注"> </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ModelList.vue',
  data() {
    return {
      tableData: []
    }
  }
}
</script>

<style scoped></style>
