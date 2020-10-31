<template>
  <div id="designBase">
    <el-card>
      <div id="search">
        <el-input v-model="search" placeholder="按描述搜索" style="width: 300px" @input="pageList" />
      </div>
      <div id="actionButton" style="margin-left:73%;margin-bottom: 20px;margin-top: -40px">
        <el-button type="primary">导入</el-button>
        <el-button type="primary" @click="handleAdd('addForm')">增加</el-button>
        <el-button type="success" :disabled="disabled.edit" @click="visible.editDialog = true">编辑</el-button>
        <el-popconfirm icon="el-icon-info" iconColor="red" title="是否删除所选设计准则" style="margin-left: 20px" @onConfirm="handleDeleteCommit">
          <el-button type="danger" :disabled="disabled.delete" slot="reference">删除</el-button>
        </el-popconfirm>
      </div>
      <div id="table">
        <el-table
          :data="tableData"
          border
          style="width: 100%"
          @selection-change="handleSelection"
          :default-sort="({ prop: 'type', order: '' }, { prop: 'id', order: '' }, { prop: 'element', order: '' })"
        >
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="id" label="序号" width="180" sortable> </el-table-column>
          <el-table-column prop="element" label="要素" width="180" :filters="filterData.element" :filter-method="filterElement" sortable>
            <!--todo: 筛选功能存在bug，依旧分页显示-->
          </el-table-column>
          <el-table-column prop="type" label="类别" width="180" sortable :filters="filterData.type" :filter-method="filterElement"> </el-table-column>
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
    <div id="add">
      <el-dialog title="添加新的设计准则" :visible.sync="visible.addDialog" center @close="resetForm('addForm')">
        <el-form :model="addForm" :rules="rules" ref="addForm">
          <el-form-item label="要素" label-width="120px" prop="type">
            <el-select v-model="addForm.element" placeholder="请选择" @change="test">
              <el-option v-for="item in options.element" :key="item.value" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <!--todo: 类型和要素没有关联-->
          <el-form-item label="类型" label-width="120px" prop="type">
            <el-cascader v-model="addForm.type" :options="options.type" :show-all-levels="false" @change="test"> </el-cascader>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="edit">
      <el-dialog title="编辑设计准则" :visible.sync="visible.editDialog" center>
        <el-form :model="editForm" :rules="rules" ref="editForm">
          <el-form-item label="要素" label-width="120px" prop="type">
            <el-select v-model="editForm.element" placeholder="请选择">
              <el-option v-for="item in options.element" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="类型" label-width="120px" prop="type">
            <el-cascader v-model="editForm.type" :options="options.type" :show-all-levels="false"> </el-cascader>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="editForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="delete">
      <el-dialog title="删除设计准则" :visible.sync="visible.deleteDialog" center>
        <span>是否删除以下 {{ deleteData.length }} 条设计准则</span>
        <el-card style="margin-top: 10px">
          <el-table :data="deleteData" border>
            <el-table-column property="id" label="序号" width="50"></el-table-column>
            <el-table-column property="type" label="类别" width="150"></el-table-column>
            <el-table-column property="describe" label="描述"></el-table-column>
          </el-table>
        </el-card>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.deleteDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleDeleteCommit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="upload"></div>
  </div>
</template>

<script>
export default {
  name: 'DesignBase.vue',
  data() {
    return {
      tableData: [],
      filterData: {
        element: [
          { text: '接口相关设计', value: '接口相关设计' },
          { text: '功能处理相关设计', value: '功能处理相关设计' },
          { text: '功能划分相关设计', value: '功能划分相关设计' },
          { text: '状态迁移相关设计', value: '状态迁移相关设计' },
          { text: '其他设计', value: '其他设计' }
        ],
        type: [
          { text: '接口相关设计', value: '接口相关设计' },
          { text: '功能处理相关设计', value: '功能处理相关设计' },
          { text: '功能划分相关设计', value: '功能划分相关设计' },
          { text: '状态迁移相关设计', value: '状态迁移相关设计' },
          { text: '其他设计', value: '其他设计' }
        ]
      },
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      search: '', //搜索框
      visible: {
        addDialog: false,
        deleteDialog: false,
        editDialog: false
      },
      disabled: {
        edit: true,
        delete: true
      },
      editForm: {
        //修改时使用
        name: '',
        type: '',
        describe: '',
        element: ''
      },
      addForm: {
        //添加使用
        name: '',
        type: [],
        describe: '',
        element: ''
      },
      deleteData: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        element: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      options: {
        element: [
          {
            value: '接口相关设计',
            label: '接口相关设计'
          },
          {
            value: '功能处理相关设计',
            label: '功能处理相关设计'
          },
          {
            value: '功能划分相关设计',
            label: '功能划分相关设计'
          },
          {
            value: '状态迁移相关设计',
            label: '状态迁移相关设计'
          },
          {
            value: '其他设计',
            label: '其他设计'
          }
        ],
        type: [
          {
            value: '接口相关设计',
            label: '接口相关设计',
            children: [
              {
                value: '与硬件相关接口设计',
                label: '与硬件相关接口设计'
              },
              {
                value: '软件模块间接口设计',
                label: '软件模块间接口设计'
              },
              {
                value: '人机接口设计',
                label: '人机接口设计'
              },
              {
                value: '数据设计',
                label: '数据设计'
              },
              {
                value: '人因安全性设计',
                label: '人因安全性设计'
              }
            ]
          },
          {
            value: '功能处理相关设计',
            label: '功能处理相关设计',
            children: [
              {
                value: '设计可追踪性',
                label: '设计可追踪性'
              },
              {
                value: '过程设计',
                label: '过程设计'
              },
              {
                value: '性能约束设计',
                label: '性能约束设计'
              }
            ]
          },
          {
            value: '功能划分相关设计',
            label: '功能划分相关设计',
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
              }
            ]
          },
          {
            value: '状态迁移相关设计',
            label: '状态迁移相关设计',
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
            value: '其他设计',
            label: '其他设计',
            children: [
              {
                value: '编码规范',
                label: '编码规范'
              }
            ]
          }
        ]
      }
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/design_criteria_list')
        .then(response => {
          // console.log(response.data.item_list)
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
      // 处理数据，根据表格中name字段来筛选
      let list = this.data.filter((item, index) => item.describe.includes(this.search))
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
    filterType(value, row) {
      console.log(value, row)
      return row.type === value
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.addForm.element = ''
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
      console.log(val)
      // 编辑按钮
      if (val.length === 1) {
        this.disabled.edit = false
        this.editForm = val[0]
      } else {
        this.disabled.edit = true
      }
      // 删除按钮
      if (val.length === 0) {
        this.disabled.delete = true
      } else {
        this.disabled.delete = false
        this.deleteData = val
      }
    },
    handleAdd(formName) {
      this.visible.addDialog = true
    },
    handleAddCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/add_design_criteria', this.addForm)
            .then(response => {
              if (response.data.error_code === 0) {
                alert('添加成功')
                this.pageList()
              } else {
                console.log(response.data)
              }
            })
            .catch(function(error) {
              console.log(error)
            })
          this.visible.addDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleEditCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/edit_design_criteria', this.editForm)
            .then(response => {
              if (response.data.error_code === 0) {
                alert('修改成功')
                this.pageList()
              } else {
                console.log(response.data)
              }
            })
            .catch(function(error) {
              console.log(error)
            })
          this.visible.editDialog = false
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    handleDeleteCommit() {
      this.$http
        .post('http://127.0.0.1:8000/api/delete_design_criteria', this.deleteData)
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            alert('删除成功')
            this.pageList()
            this.visible.deleteDialog = false
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    test() {
      console.log(this.addForm)
    }
  }
}
</script>

<style scoped></style>
