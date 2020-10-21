<template>
  <div id="generalCriteria">
    <el-card style="margin-left: 10px;margin-right: 10px">
      <div class="divForm">
        <span>选择规则</span>
        <el-button style="margin-left: 50px" type="primary" v-show="buttonShow" @click="handleReset">确定</el-button>
        <el-checkbox-group v-model="radio" v-show="buttonShow" style="margin-left: 250px;margin-top: -25px">
          <el-checkbox :label="1">状态机</el-checkbox>
          <el-checkbox :label="2">时序图</el-checkbox>
          <el-checkbox :label="3">用例图</el-checkbox>
          <el-checkbox :label="4">活动图</el-checkbox>
        </el-checkbox-group>
        <el-table
          ref="multipleTable"
          :data="tableData"
          tooltip-effect="dark"
          style="width: 100%;margin-top: 20px"
          @selection-change="handleSelectionChange"
          border
          :header-cell-style="{ background: '#eef1f6', color: '#606266' }"
        >
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column label="序号" width="180px" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.id }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="类型"
            width="180"
            :filters="[
              { text: '外部接口', value: '外部接口' },
              { text: '功能处理', value: '功能处理' },
              { text: '功能层次', value: '功能层次' },
              { text: '状态迁移', value: '状态迁移' },
              { text: '其他', value: '其他' }
            ]"
            :filter-method="filterGroup"
          >
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.type }}</span>
            </template>
            <!--          <template slot-scope="scope">-->
            <!--            <el-tag :type="scope.row.type === '属性一' ? 'primary' : 'success'" disable-transitions>{{ scope.row.type }}</el-tag>-->
            <!--          </template>-->
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
          <!--        <el-table-column label="操作" align="center">-->
          <!--          <template slot-scope="scope">-->
          <!--            &lt;!&ndash;            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>&ndash;&gt;-->
          <!--            <el-button size="mini" type="primary" @click="handleVerify(scope.$index, scope.row)">验证</el-button>-->
          <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看完整验证信息</el-button>-->
          <!--          </template>-->
          <!--        </el-table-column>-->
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
          style="margin-left: 30%;margin-top: 20px"
        >
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'GeneralCriteria.vue',
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: [],
      buttonShow: false,
      radio: []
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/analysis_rule_list')
        .then(response => {
          // console.log(response.data.design_list)
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
    },
    handleSelectionChange(val) {
      // this.multipleSelection = val
      console.log(val)
      if (val.length > 0) {
        this.buttonShow = true
      } else {
        this.buttonShow = false
      }
    },
    filterGroup(value, row) {
      // console.log(value, row)
      return row.type === value
    }
  }
}
</script>

<style scoped></style>
