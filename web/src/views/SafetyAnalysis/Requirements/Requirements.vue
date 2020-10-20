<template>
  <div id="generalCriteria">
    <el-card style="margin-left: 10px;margin-right: 10px">
      <div class="divForm">
        <span>选择规则</span>
        <el-button style="margin-left: 50px" type="primary" v-show="buttonShow" @click="handleReset">确定</el-button>
        <el-radio-group v-model="radio" v-show="buttonShow" style="margin-left: 20px">
          <el-radio :label="1">状态机</el-radio>
          <el-radio :label="2">时序图</el-radio>
          <el-radio :label="3">用例图</el-radio>
          <el-radio :label="4">活动图</el-radio>
        </el-radio-group>
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
          <el-table-column label="失效描述" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="改进措施" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.content }}</span>
            </template>
          </el-table-column>
          <el-table-column label="软件安全性需求" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.type }}</span>
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
      tableData: [
        {
          id: '1',
          name: '软件失效描述',
          content: '针对失效的改进措施',
          type: '改进措施对应的具体软件需求'
        },
        {
          id: '2',
          name: '软件失效描述',
          content: '针对失效的改进措施',
          type: '改进措施对应的具体软件需求'
        },
        {
          id: '3',
          name: '软件失效描述',
          content: '针对失效的改进措施',
          type: '改进措施对应的具体软件需求'
        },
        {
          id: '4',
          name: '软件失效描述',
          content: '针对失效的改进措施',
          type: '改进措施对应的具体软件需求'
        }
      ],
      buttonShow: false,
      radio: '3'
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      // this.$http
      //   .get('http://127.0.0.1:8000/api/analysis_rule_list')
      //   .then(response => {
      //     // console.log(response.data.design_list)
      //     this.data = response.data.analysis_list
      //     this.getList()
      //   })
      //   .catch(function(error) {
      //     console.log(error)
      //   })
      this.data = this.tableData
      this.getList()
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
