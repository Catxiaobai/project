<template>
  <div id="verification">
    <el-card style="margin-right: 10px;margin-left: 10px">
      <el-table :data="tableData" border style="width: 100%" header-row-class-name="tableHead">
        <el-table-column prop="id" label="序号" width="50"> </el-table-column>
        <el-table-column prop="element" label="要素" width="150">
          <template slot-scope="scope">
            <span style="margin-left: 10px" v-show="!test1">{{ scope.row.group }}</span>
            <el-select v-model="scope.row.element" placeholder="请选择" v-show="test1">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类别" width="150">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === '硬件相关' ? 'primary' : 'success'" disable-transitions v-show="!test2">
              {{ scope.row.type }}
            </el-tag>
            <el-cascader v-model="scope.row.type" :options="options2" @change="handleChange" :show-all-levels="false" v-show="test2"> </el-cascader>
          </template>
        </el-table-column>
        <el-table-column prop="criteria" label="准则描述" width="180">
          <template slot-scope="scope">
            <span style="margin-left: 10px" v-show="!test3">{{ scope.row.criteria }}</span>
            <textarea placeholder="输入准则描述" v-model="scope.row.criteria" v-show="test3"></textarea>
          </template>
        </el-table-column>
        <el-table-column prop="apply" label="适用性" width="300">
          <template slot-scope="scope">
            <el-radio-group v-model="scope.row.apply">
              <el-radio :label="3">适用</el-radio>
              <el-radio :label="6">不适用</el-radio>
              <el-radio :label="9">部分适用</el-radio>
            </el-radio-group>
          </template>
        </el-table-column>
        <el-table-column prop="conform" label="符合性" width="170">
          <template slot-scope="scope">
            <el-radio-group v-model="scope.row.conform">
              <el-radio :label="1">符合</el-radio>
              <el-radio :label="2">不符合</el-radio>
            </el-radio-group>
          </template>
        </el-table-column>
        <el-table-column prop="problem" label="问题描述">
          <template slot-scope="scope">
            <span style="margin-left: 10px" v-show="!test3">{{ scope.row.problem }}</span>
            <textarea placeholder="输入问题描述" v-model="scope.row.problem" v-show="test3"></textarea>
          </template>
        </el-table-column>
      </el-table>
      <el-button icon="el-icon-plus" style="width: 100%" @click="handleAdd"></el-button>
    </el-card>
    <el-button type="primary" style="margin-left: 50%">保存</el-button>
  </div>
</template>

<script>
export default {
  name: 'Verification.vue',
  data() {
    return {
      tableData: [
        // {
        //   id: '序号',
        //   element: '要素',
        //   type: '类别',
        //   criteria: '准则描述',
        //   apply: '适用性',
        //   conform: '符合性',
        //   problem: '问题描述'
        // },
        // {
        //   id: '序号',
        //   element: '要素',
        //   type: '类别',
        //   criteria: '准则描述',
        //   apply: '适用性',
        //   conform: '符合性',
        //   problem: '问题描述'
        // },
        // {
        //   id: '序号',
        //   element: '要素',
        //   type: '类别',
        //   criteria: '准则描述',
        //   apply: '适用性',
        //   conform: '符合性',
        //   problem: '问题描述'
        // },
        // {
        //   id: '序号',
        //   element: '要素',
        //   type: '类别',
        //   criteria: '准则描述',
        //   apply: '适用性',
        //   conform: '符合性',
        //   problem: '问题描述'
        // }
      ],
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
      testId: 0,
      test1: true,
      test2: true,
      test3: true,
      radio: 3,
      radio2: 2
    }
  },
  methods: {
    handleAdd() {
      this.tableData.push({
        id: this.testId + 1,
        element: '',
        type: '',
        criteria: '',
        apply: '',
        conform: '',
        problem: ''
      })
      this.testId++
    }
  }
}
</script>

<style lang="scss">
.tableHead {
  font-weight: bold;
  color: black;
  //font-family: 华文行楷;
}
</style>
