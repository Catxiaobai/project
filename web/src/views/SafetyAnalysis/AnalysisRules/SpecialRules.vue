<template>
  <div id="specialRules">
    <el-card style="margin-left: 10px;margin-right: 10px">
      <div id="actionButton" style="margin-left: 50px;margin-bottom: 20px">
        <el-popconfirm icon="el-icon-loading" iconColor="blue" title="是否将所选规则加入通用分析规则库？" @onConfirm="handleSelectCommit">
          <el-button type="primary" :disabled="disabled.select" slot="reference">选择加入通用分析规则库</el-button>
        </el-popconfirm>
        <el-popconfirm icon="el-icon-info" iconColor="red" title="是否删除所选规则" style="margin-left: 20px" @onConfirm="handleDeleteCommit">
          <el-button type="danger" :disabled="disabled.delete" slot="reference">删除</el-button>
        </el-popconfirm>
        <el-button type="primary" style="margin-left: 60%" @click="handleAdd('addForm')">增加项目分析规则</el-button>
      </div>
      <div id="table">
        <el-table :data="tableData" border style="width: 100%" @selection-change="handleSelection" @filter-change="handleFilterChange">
          <el-table-column type="selection" width="40px"> </el-table-column>
          <el-table-column prop="id" label="序号" width="80"> </el-table-column>
          <el-table-column prop="type" label="类别" width="180" :filters="filterData" column-key="type"> </el-table-column>
          <el-table-column prop="name" label="名称" width="180"> </el-table-column>
          <el-table-column prop="describe" label="描述" width="180"> </el-table-column>
          <el-table-column prop="remark" label="备注"> </el-table-column>
          <el-table-column prop="belong" label="所属"></el-table-column>
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
    <div id="select">
      <el-dialog title="选择" :visible.sync="visible.selectDialog">
        <span>是否选择以下 {{ selectData.length }} 条分析规则</span>
        <el-card style="margin-top: 10px">
          <el-table :data="selectData" border>
            <el-table-column property="id" label="序号" width="50"></el-table-column>
            <el-table-column property="type" label="类别" width="150"></el-table-column>
            <el-table-column property="name" label="名称"></el-table-column>
          </el-table>
        </el-card>
        <div slot="footer" class="dialog-footer">
          <el-button @click="visible.deleteDialog = false">取 消</el-button>
          <el-button type="primary" @click="handleSelectCommit">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="add">
      <el-dialog title="添加新的分析规则" :visible.sync="visible.addDialog" center>
        <el-form :model="addForm" :rules="rules" ref="addForm">
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="addForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="类型" label-width="120px" prop="type">
            <el-select v-model="addForm.type" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="描述" label-width="120px" prop="describe">
            <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入文字描述"> </el-input>
          </el-form-item>
          <el-form-item label="备注" label-width="120px" prop="remark">
            <el-input v-model="addForm.remark" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入备注"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="delete">
      <el-dialog title="删除分析规则" :visible.sync="visible.deleteDialog" center>
        <span>是否删除以下 {{ deleteData.length }} 条分析规则</span>
        <el-card style="margin-top: 10px">
          <el-table :data="deleteData" border>
            <el-table-column property="id" label="序号" width="50"></el-table-column>
            <el-table-column property="type" label="类别" width="150"></el-table-column>
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
  name: 'SpecialRules.vue',
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
        addDialog: false,
        selectDialog: false,
        deleteDialog: false
      },
      disabled: {
        select: true,
        delete: true
      },
      selectData: [],
      deleteData: [],
      addForm: {
        //添加使用
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
      addData: [],
      filterData: [
        { text: '外部接口', value: '外部接口' },
        { text: '功能处理', value: '功能处理' },
        { text: '功能层次', value: '功能层次' },
        { text: '状态迁移', value: '状态迁移' },
        { text: '其他', value: '其他' }
      ]
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
      let list = this.data
      if (this.data.length > 0) {
        list = this.data.filter((item, index) => item.name.includes(this.search))
      }
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
    handleFilterChange(value) {
      console.log(value)
      // if (value['element']) {
      //   this.filterSearch = value['element']
      //   let list = this.data.filter((item, index) => item.element.includes(this.filterSearch))
      //   this.tableData = list.filter(
      //     (item, index) => index < this.pagination.page * this.pagination.limit && index >= this.pagination.limit * (this.pagination.page - 1)
      //   )
      //   this.pagination.total = list.length
      // }
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
      if (val.length === 0) {
        this.disabled.select = true
        this.disabled.delete = true
      } else {
        this.disabled.select = false
        this.selectData = val
        this.disabled.delete = false
        this.deleteData = val
      }
    },
    getItemInfo() {
      this.itemInfo = this.$store.state.item
      console.log('ss', this.itemInfo)
    },
    handleSelectCommit() {
      console.log('ss', this.selectData)
      // this.getItemInfo()
      // this.visible.selectDialog = false
      this.$http
        .post('http://127.0.0.1:8000/api/add_analysis_rule_from_item', this.selectData)
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            alert('添加成功（已自动过滤已存在规则）')
            this.pageList()
          } else {
            alert(response.data)
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    handleAdd(formName) {
      this.visible.addDialog = true
    },
    handleAddCommit(formName) {
      this.addData = []
      this.addData.push(this.addForm)
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/add_rule', { selectData: this.addData, item: this.itemInfo, belong: '专用' })
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
    }
  }
}
</script>

<style scoped></style>
