<template>
  <div id="instantiate">
    <el-card style="margin-left: 10px;margin-right: 10px">
      <div id="actionButton" style="margin-left: 50px;margin-bottom: 20px">
        <el-button type="success" :disabled="disabled.edit" @click="handleSelect">选择实例化</el-button>
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="id" label="序号" width="180"> </el-table-column>
          <el-table-column prop="type" label="类别" width="180" :filters="filterData" :filter-method="filterType">
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
      <el-dialog title="选择" :visible.sync="visible.editDialog">
        <span>对分析规则 [id:{{ editForm.id }}, type: {{ editForm.type }}, name: {{ editForm.name }}] 进行实例化</span>
        <el-table :data="caseData" border>
          <el-table-column property="id" label="序号" width="50"></el-table-column>
          <el-table-column property="element" label="要素" width="150"></el-table-column>
          <el-table-column property="name" label="名称" width="150"></el-table-column>
          <el-table-column property="describe" label="描述" width="150"></el-table-column>
          <el-table-column property="content" label="内容"></el-table-column>
        </el-table>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.editDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleSelectCommit">确 定</el-button>
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
        editDialog: false
      },
      disabled: {
        edit: true,
        delete: true
      },
      caseData: [],
      editForm: {
        id: '',
        name: '',
        type: '',
        describe: '',
        remark: ''
      },
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        remark: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }],
        type: [{ required: true, message: '不能为空', trigger: 'blur' }]
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
      addData: []
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
        .post('http://127.0.0.1:8000/api/rules_list', this.itemInfo.item_id)
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
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('ss', this.itemInfo)
    },
    handleAdd(formName) {
      this.visible.addDialog = true
      this.resetForm(formName)
    },
    handleAddCommit(formName) {
      this.addData = []
      this.addData.push(this.addForm)
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/add_rule', { selectData: this.addData, item: this.itemInfo })
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
    handleDeleteCommit() {
      this.$http
        .post('http://127.0.0.1:8000/api/delete_rule', this.deleteData)
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
    handleSelect() {
      this.$http
        .post('http://127.0.0.1:8000/api/case_list', this.itemInfo.item_id)
        .then(response => {
          this.caseData = response.data.case_list
        })
        .catch(function(error) {
          console.log(error)
        })
      this.visible.editDialog = true
    }
  }
}
</script>

<style scoped></style>
