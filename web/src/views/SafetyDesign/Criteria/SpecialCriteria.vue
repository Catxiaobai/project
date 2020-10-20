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
              <span style="margin-left: 10px" v-show="!test1">{{ scope.row.group }}</span>
              <el-select v-model="scope.row.group" placeholder="请选择" v-show="test1">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="类别" width="180">
            <template slot-scope="scope">
              <el-tag :type="scope.row.type === '硬件相关' ? 'primary' : 'success'" disable-transitions v-show="!test2">
                {{ scope.row.type }}
              </el-tag>
              <el-cascader v-model="scope.row.type" :options="options2" @change="handleChange" :show-all-levels="false" v-show="test2"> </el-cascader>
            </template>
          </el-table-column>
          <el-table-column label="准则描述" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px" v-show="!test3">{{ scope.row.content }}</span>
              <textarea placeholder="输入准则描述" v-model="scope.row.content" v-show="test3"></textarea>
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
      tableData: [],
      buttonShow: false,
      options: [
        {
          value: '接口相关',
          label: '接口相关'
        },
        {
          value: '功能处理',
          label: '功能处理'
        },
        {
          value: '功能划分',
          label: '功能划分'
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
          value: '接口相关',
          label: '接口相关',
          children: [
            {
              value: '与硬件相关',
              label: '与硬件相关'
            },
            {
              value: '软件模块间接口',
              label: '软件模块间接口'
            },
            {
              value: '人机接口',
              label: '人机接口'
            },
            {
              value: '数据设计',
              label: '数据设计'
            },
            {
              value: '人因安全设计',
              label: '人因安全设计'
            }
          ]
        },
        {
          value: '功能处理',
          label: '功能处理',
          children: [
            {
              value: '设计可追踪性',
              label: '设计可追踪性'
            },
            {
              value: '设计可追踪性',
              label: '设计可追踪性'
            },
            {
              value: '性能约束设计',
              label: '性能约束设计'
            }
          ]
        },
        {
          value: '功能划分',
          label: '功能划分',
          children: [
            {
              value: '独立性设计',
              label: '独立性设计'
            },
            {
              value: '体系结构设计',
              label: '体系结构设计'
            },
            {
              value: '中断设计',
              label: '中断设计'
            },
            {
              value: '同步设计',
              label: '同步设计'
            },
            {
              value: '人因安全设计',
              label: '人因安全设计'
            }
          ]
        },
        {
          value: '状态迁移',
          label: '状态迁移',
          children: [
            {
              value: '交叉传输机制设计',
              label: '交叉传输机制设计'
            },
            {
              value: '表决监控机制设计',
              label: '表决监控机制设计'
            }
          ]
        },
        {
          value: '其他',
          label: '其他',
          children: [
            {
              value: '编码规范',
              label: '编码规范'
            }
          ]
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
      return row.group === value
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
      this.data[this.test_id - 1].type = row.type[1]
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
