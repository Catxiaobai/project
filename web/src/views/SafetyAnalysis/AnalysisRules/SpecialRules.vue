<template>
  <div id="specialCriteria">
    <el-card style="margin-left: 10px;margin-right: 10px">
      <div class="divForm">
        <span>选择规则</span>
        <el-button style="margin-left: 50px" type="primary" v-show="buttonShow" @click="handleReset">加入软件安全性设计准则库</el-button>
        <!--        <el-button type="primary" icon="el-icon-plus" style="float: right;margin-bottom: 10px">添加新准则</el-button>-->
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
              <span style="margin-left: 10px" v-show="!test1">{{ scope.row.type }}</span>
              <el-select v-model="scope.row.type" placeholder="请选择" v-show="test1">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="适用模型" width="180">
            <template slot-scope="scope">
              <span style="margin-left: 10px" v-show="!test1">{{ scope.row.group }}</span>
              <el-select v-model="scope.row.group" placeholder="请选择" v-show="test1">
                <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="所属通用规则" width="180">
            <template slot-scope="scope">
              <span style="margin-left: 10px" v-show="!test1">{{ scope.row.name }}</span>
              <el-select v-model="scope.row.name" placeholder="请选择" v-show="test1">
                <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </template>
          </el-table-column>
          <!--          <el-table-column label="类别" width="180">-->
          <!--            <template slot-scope="scope">-->
          <!--              <el-tag :type="scope.row.type === '硬件相关' ? 'primary' : 'success'" disable-transitions v-show="!test2">-->
          <!--                {{ scope.row.type }}-->
          <!--              </el-tag>-->
          <!--              <el-cascader v-model="scope.row.type" :options="options2" @change="handleChange" :show-all-levels="false" v-show="test2"> </el-cascader>-->
          <!--            </template>-->
          <!--          </el-table-column>-->
          <el-table-column label="规则描述" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px" v-show="!test3">{{ scope.row.content }}</span>
              <textarea placeholder="输入规则描述" v-model="scope.row.content" v-show="test3"></textarea>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center">
            <template slot-scope="scope">
              <!--              <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>-->
              <el-button size="mini" type="success" @click="handleSave(scope.$index, scope.row)">保存</el-button>
              <el-button size="mini" type="danger" @click="handleShow(scope.$index, scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button style="width: 100%" icon="el-icon-plus" @click="addCriteria"></el-button>
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
  name: 'SpecialCriteria.vue',
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: [
        {
          id: 0,
          name: '通用规则1',
          content: '这是规则描述',
          group: '状态机',
          type: '外部接口'
        }
      ],
      buttonShow: false,
      options: [
        {
          value: '外部接口',
          label: '外部接口'
        },
        {
          value: '功能处理',
          label: '功能处理'
        },
        {
          value: '功能层次',
          label: '功能层次'
        },
        {
          value: '状态迁移',
          label: '状态迁移'
        },
        {
          value: '其他',
          label: '其他'
        }
      ],
      options2: [
        {
          value: '状态机',
          label: '状态机'
        },
        {
          value: '用例图',
          label: '用例图'
        },
        {
          value: '时序图',
          label: '时序图'
        },
        {
          value: '活动图',
          label: '活动图'
        }
      ],
      options3: [
        {
          value: '通用规则1',
          label: '通用规则1'
        },
        {
          value: '通用规则2',
          label: '通用规则2'
        },
        {
          value: '通用规则3',
          label: '通用规则3'
        },
        {
          value: '通用规则4',
          label: '通用规则4'
        }
      ],
      value: '',
      test1: true,
      test2: true,
      test3: true,
      test_id: 1
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      // this.$http
      //   .get('http://127.0.0.1:8000/api/design_criteria_list')
      //   .then(response => {
      //     // console.log(response.data.design_list)
      //     this.data = response.data.design_list
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
    },
    addCriteria() {
      this.test1 = true
      this.test2 = true
      this.test3 = true
      this.data.push({
        id: this.test_id,
        name: '',
        content: '',
        group: '',
        type: ''
      })
      this.getList()
    },
    handleSave(index, row) {
      console.log(index, row)
      console.log(this.data)
      this.data[this.test_id - 1].content = row.content
      this.data[this.test_id - 1].group = row.group
      this.data[this.test_id - 1].type = row.type
      this.test_id++
      this.test1 = false
      this.test2 = false
      this.test3 = false
    },
    handleChange(value) {
      console.log(value)
    }
  }
}
</script>

<style scoped></style>
