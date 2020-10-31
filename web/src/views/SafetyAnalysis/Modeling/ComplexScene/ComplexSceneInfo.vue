<template>
  <div id="complexSceneInfo">
    <el-card>
      <div id="search">
        <el-input v-model="search" placeholder="按名称搜索" style="width: 300px" @input="pageList" />
      </div>
      <div id="actionButton" style="margin-left:73%;margin-bottom: 20px;margin-top: -40px">
        <el-button type="primary">导入</el-button>
        <el-button type="primary" @click="handleAdd('addForm')">增加</el-button>
        <el-button type="success" :disabled="disabled.edit" @click="visible.editDialog = true">编辑</el-button>
        <el-button type="danger" :disabled="disabled.delete" @click="visible.deleteDialog = true">删除</el-button>
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="id" label="序号" width="80"> </el-table-column>
          <el-table-column prop="element" label="类别" width="180" :filters="filterData" :filter-method="filterType">
            <!--todo: 筛选功能存在bug-->
          </el-table-column>
          <el-table-column prop="name" label="名称" width="180"> </el-table-column>
          <el-table-column prop="describe" label="描述" width="180" :show-overflow-tooltip="true">
            <!--todo: 过长不好看-->
          </el-table-column>
          <el-table-column prop="content" label="规格化描述"> </el-table-column>
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
    <!--    <div id="show"></div>-->
    <div id="add">
      <el-dialog title="添加新的场景" :visible.sync="visible.addDialog" center @close="resetForm('addForm')">
        <el-form :model="addForm" :rules="rules" ref="addForm">
          <el-form-item label="类别" label-width="120px" prop="element">
            <el-select v-model="addForm.element" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="addForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
          <el-form-item label="规格化描述" label-width="120px" prop="content">
            <el-input v-model="addForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入备注"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="edit">
      <el-dialog title="编辑场景" :visible.sync="visible.editDialog" center>
        <el-form :model="editForm" :rules="rules" ref="editForm">
          <el-form-item label="要素" label-width="120px" prop="element">
            <el-select v-model="editForm.element" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="editForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="editForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
          <el-form-item label="规格化描述" label-width="120px" prop="content">
            <el-input v-model="editForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入备注"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="delete">
      <el-dialog title="删除场景" :visible.sync="visible.deleteDialog" center>
        <span>是否删除以下 {{ deleteData.length }} 条场景</span>
        <el-card style="margin-top: 10px">
          <el-table :data="deleteData" border>
            <el-table-column property="id" label="序号" width="50"></el-table-column>
            <el-table-column property="element" label="要素" width="150"></el-table-column>
            <el-table-column property="name" label="名称"></el-table-column>
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
  name: 'ComplexSceneInfo.vue',
  data() {
    return {
      tableData: [],
      filterData: [
        { text: '外部交联环境', value: '外部交联环境' },
        { text: '功能处理', value: '功能处理' },
        { text: '功能层次', value: '功能层次' },
        { text: '状态迁移', value: '状态迁移' }
      ],
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
        id: '',
        name: '',
        type: '',
        describe: '',
        content: '',
        element: ''
      },
      addForm: {
        //添加使用
        name: '',
        describe: '',
        content: '',
        element: '',
        type: 'complex'
      },
      deleteData: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        content: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }],
        element: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      options: [
        {
          value: '外部交联环境',
          label: '外部交联环境'
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
        }
      ],
      itemInfo: ''
    }
  },
  created() {
    this.getItemInfo()
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .post('http://127.0.0.1:8000/api/scenes_list', this.itemInfo.id)
        .then(response => {
          // console.log(response.data.analysis_list)
          this.data = response.data.scenes_list
          // 筛选出子场景
          this.data = this.data.filter((item, index) => item.type.includes('complex'))
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
    filterType(value, row) {
      console.log(value, row)
      return row.type === value
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
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
      this.resetForm(formName)
    },
    handleAddCommit(formName) {
      this.addForm.type = 'complex'
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/add_scenes', this.addForm)
            .then(response => {
              if (response.data.error_code === 0) {
                alert('添加成功')
                this.resetForm(formName)
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
            .post('http://127.0.0.1:8000/api/edit_scenes', this.editForm)
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
        .post('http://127.0.0.1:8000/api/delete_scenes', this.deleteData)
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
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('综合场景项目信息', this.itemInfo)
    }
  }
}
</script>

<style lang="scss">
.el-tooltip__popper {
  max-width: 30%;
  line-height: 130%;
  //overflow: hidden;
  display: block;
  white-space: pre-line;
}
</style>
