<template>
  <div id="instantiate">
    <el-card style="margin-left: 10px;margin-right: 10px">
      <div id="actionButton" style="margin-left: 50px;margin-bottom: 20px">
        <el-button type="success" :disabled="disabled.edit" @click="handleSelect">选择实例化</el-button>
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection" @filter-change="handleFilterChange">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="id" label="序号" width="180"> </el-table-column>
          <el-table-column prop="type" label="类别" width="180" :filters="filterData" column-key="type">
            <!--todo: 筛选功能存在bug-->
          </el-table-column>
          <el-table-column prop="name" label="名称" width="180"> </el-table-column>
          <el-table-column prop="describe" label="描述" width="180"> </el-table-column>
          <el-table-column prop="remark" label="备注"> </el-table-column>
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
    <div id="edit">
      <el-dialog title="此分析规则的实例" :visible.sync="visible.editDialog" center>
        <span>对分析规则 [id:{{ editForm.id }}, element: {{ editForm.type }}, name: {{ editForm.name }}] 进行实例化</span>
        <el-button type="primary" @click="handleAdd" style="margin-left: 30px;margin-bottom: 10px">添加实例</el-button>
        <el-popconfirm icon="el-icon-info" iconColor="red" title="是否删除所选实例" style="margin-left: 20px" @onConfirm="handleDeleteCommit">
          <el-button type="danger" :disabled="disabled.delete" slot="reference">删除</el-button>
        </el-popconfirm>
        <el-table :data="caseData" border @selection-change="handleSelectCase">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column property="element" label="要素" width="150"></el-table-column>、
          <el-table-column property="name" label="名称" width="150">
            <template slot-scope="scope">
              <el-input class="tableCell" type="textarea" autosize v-model="scope.row.name"> </el-input>
            </template>
          </el-table-column>
          <el-table-column property="describe" label="描述" width="150">
            <template slot-scope="scope">
              <el-input class="tableCell" type="textarea" autosize v-model="scope.row.describe"> </el-input>
            </template>
          </el-table-column>
          <el-table-column property="content" label="规格化描述">
            <template slot-scope="scope">
              <el-input class="tableCell" type="textarea" autosize v-model="scope.row.content"> </el-input>
            </template>
          </el-table-column>
        </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.editDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleSave">保 存</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="add">
      <!--todo:修改成可在表格内编辑的样式-->
      <el-dialog width="40%" title="添加实例" :visible.sync="visible.addDialog" append-to-body>
        <el-form :model="addForm" :rules="rules" ref="addForm" style="margin-right: 50px">
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="addForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
          <el-form-item label="规格化描述" label-width="120px" prop="content">
            <el-input v-model="addForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入规格化描述"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.addDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="delete">
      <el-dialog title="删除分析规则" :visible.sync="visible.deleteDialog" center>
        <span>是否删除以下 {{ selectCase.length }} 条实例</span>
        <el-card style="margin-top: 10px">
          <el-table :data="selectCase" border>
            <el-table-column property="id" label="序号" width="50"></el-table-column>
            <el-table-column property="element" label="类别" width="150"></el-table-column>
            <el-table-column property="name" label="名称"></el-table-column>
          </el-table>
        </el-card>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.deleteDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleDeleteCommit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Instantiate.vue',
  data() {
    return {
      tableData: [],
      itemInfo: '',
      search: '', //搜索框
      pagination: {
        limit: 7, //每页显示条数
        total: 0, //项目总数
        page: 1 //第几页
      },
      visible: {
        editDialog: false,
        addDialog: false,
        deleteDialog: false
      },
      disabled: {
        edit: true,
        delete: true
      },
      caseData: [],
      deleteData: [],
      filterData: [
        { text: '外部接口', value: '外部接口' },
        { text: '功能处理', value: '功能处理' },
        { text: '功能层次', value: '功能层次' },
        { text: '状态迁移', value: '状态迁移' },
        { text: '其他', value: '其他' }
      ],
      editForm: {
        id: '',
        name: '',
        type: '',
        describe: '',
        remark: ''
      },
      addForm: {
        element: '',
        name: '',
        describe: '',
        content: ''
      },
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        remark: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }],
        element: [{ required: true, message: '不能为空', trigger: 'blur' }],
        content: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
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
      addData: [],
      selectCase: []
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
        .post('http://127.0.0.1:8000/api/rules_list', this.itemInfo.id)
        .then(response => {
          this.data = response.data.rules_list
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
      // let list = this.data.filter((item, index) => item.name.includes(this.search))
      let list = this.data
      this.tableData = list.filter(
        (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      )
      this.pagination.total = list.length
      // console.log(this.tableData)
      if (this.tableData.length === 0) {
        alert('当前项目规则集为空，请前往设置规则集')
      }
    },
    handleFilterChange(value) {
      console.log(value)
      if (value['element']) {
        this.filterSearch = value['element']
        let list = this.data.filter((item, index) => item.element.includes(this.filterSearch))
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
      if (value['type']) {
        this.filterSearch = value['type']
        let list = this.data.filter((item, index) => item.type.includes(this.filterSearch))
        this.tableData = list.filter(
          (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
        )
        this.pagination.total = list.length
      }
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
      console.log('val', val[0])
      // 编辑按钮
      if (val.length === 1) {
        this.disabled.edit = false
        this.editForm = val[0]
      } else {
        this.disabled.edit = true
      }
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('ss', this.itemInfo)
    },
    // handleAdd(formName) {
    //   this.visible.addDialog = true
    // },
    handleAddCommit(formName) {
      this.addForm.element = this.editForm.type
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/add_case', { addData: this.addForm, rule: this.editForm })
            .then(response => {
              if (response.data.error_code === 0) {
                alert('添加成功')
                this.resetForm(formName)
                this.caseList()
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
    caseList() {
      console.log(this.editForm)
      this.$http
        .post('http://127.0.0.1:8000/api/add_case_list', this.editForm.id)
        .then(response => {
          this.caseData = response.data.case_list
          console.log('caseData', this.caseData)
          console.log('editForm', this.editForm)
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    handleDeleteCommit() {
      // this.$http
      //   .post('http://127.0.0.1:8000/api/delete_case', this.selectCase)
      //   .then(response => {
      //     console.log(response.data)
      //     if (response.data.error_code === 0) {
      //       alert('删除成功')
      //       this.caseList()
      //       this.visible.deleteDialog = false
      //     }
      //   })
      //   .catch(function(error) {
      //     console.log(error)
      //   })
      console.log('this.selectCase', this.selectCase)
      console.log('this.caseData', this.caseData)
      for (let i = 0; i < this.caseData.length; i++) {
        for (let j = 0; j < this.selectCase.length; j++) {
          if (this.caseData[i] === this.selectCase[j]) {
            this.deleteData.push(this.caseData[i].id)
            this.caseData.splice(this.caseData[i], 1)
          }
        }
      }
    },
    handleSelect() {
      this.caseList()
      this.visible.editDialog = true
    },
    handleEditCommit() {
      this.visible.editDialog = false
    },
    handleSelectCase(val) {
      console.log('case', val)
      // 删除按钮
      if (val.length === 0) {
        this.disabled.delete = true
      } else {
        this.disabled.delete = false
        this.selectCase = val
      }
    },
    handleAdd() {
      let rule_id = this.editForm.id
      let element = this.editForm.type
      this.caseData.push({
        id: -100,
        rule_id: rule_id,
        element: element
      })
    },
    handleSave() {
      console.log(this.caseData)
      this.$http
        .post('http://127.0.0.1:8000/api/add_case', { caseData: this.caseData, rule: this.editForm, deleteData: this.deleteData })
        .then(response => {
          if (response.data.error_code === 0) {
            alert('保存成功')
            this.caseList()
            this.deleteData = []
          } else {
            console.log(response.data)
            alert(response.data.error_message)
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped></style>
<style lang="scss">
.tableCell {
  .el-textarea__inner {
    border: none;
    resize: none;
  }
}
</style>
