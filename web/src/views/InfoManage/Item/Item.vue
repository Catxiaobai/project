<template>
  <div id="item">
    <el-card class="tableTitle">
      <span style="font-size: 20px">当前系统共有{{ total }}个项目</span>
      <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <el-button size="20px" type="primary" style="margin-left: 350px" @click="handleAdd('addForm')" icon="el-icon-plus">创建新项目</el-button>
      <el-button size="20px" type="primary" @click="handleAddBasedExist('addForm2')" icon="el-icon-plus">基于已有项目新建</el-button>
      <el-table :data="tableData" style="width: 100%;margin-top: 40px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
        <el-table-column label="序号" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.item_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="名称" width="180px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.item_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="项目介绍" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.item_introduction }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="handleOpen(scope.$index, scope.row)">进入</el-button>
            <!--            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>-->
            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 2, 5, 7, 10]"
        :page-size="limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-left: 30%;margin-top: 30px"
      >
      </el-pagination>
    </el-card>
    <div id="add">
      <el-dialog title="添加新的项目" :visible.sync="visible.addDialog" center @close="resetForm('addForm')">
        <el-form :model="addForm" :rules="rules" ref="addForm">
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="addForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="项目介绍" label-width="120px" prop="introduction">
            <el-input v-model="addForm.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="add2">
      <el-dialog title="基于已有项目添加" :visible.sync="visible.addDialog2" center>
        <el-form :model="addForm2" :rules="rules" ref="addForm">
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="addForm2.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="项目介绍" label-width="120px" prop="introduction">
            <el-input v-model="addForm2.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
          </el-form-item>
          <el-form-item label="基于的项目" label-width="120px" prop="basedItem">
            <el-select v-model="addForm2.basedItem" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
            </el-select>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleAddCommit2('addForm2')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div id="edit">
      <el-dialog title="编辑项目" :visible.sync="visible.editDialog" center>
        <el-form :model="editForm" :rules="rules" ref="editForm">
          <el-form-item label="名称" label-width="120px" prop="name">
            <el-input v-model="editForm.name" clearable placeholder="请输入名称"></el-input>
          </el-form-item>
          <el-form-item label="项目介绍" label-width="120px" prop="introduction">
            <el-input v-model="editForm.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
          <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: [], //项目表
      showItem: {}, //查看项目
      visible: {
        addDialog: false,
        addDialog2: false,
        deleteDialog: false,
        editDialog: false
      },
      editForm: {
        //修改时使用
        id: '',
        name: '',
        introduction: ''
      },
      addForm: {
        //添加使用
        name: '',
        introduction: ''
      },
      addForm2: {
        //添加使用
        name: '',
        introduction: '',
        basedItem: ''
      },
      deleteData: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        introduction: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      options: []
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      this.$http
        .get('http://127.0.0.1:8000/api/item_list')
        .then(response => {
          this.data = response.data.item_list
          for (let i = 0; i < this.data.length; i++) {
            this.options.push({ value: this.data[i].item_name, label: this.data[i].item_name })
          }
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    // 处理数据
    getList() {
      let list = this.data.filter((item, index) => item.item_introduction.includes(this.search))
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    handleOpen(index, row) {
      // console.log(row)
      this.bus.$emit('itemInfo', row)
      this.$store.commit('changeItem', row)
    },
    handleAdd(formName) {
      this.visible.addDialog = true
    },
    handleAddCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/add_item', this.addForm)
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
    handleAddCommit2(formName) {
      console.log(formName)
      // todo: 基于已有项目创建
      // this.$refs[formName].validate(valid => {
      //   if (valid) {
      //     this.$http
      //       .post('http://127.0.0.1:8000/api/add_item', this.addForm)
      //       .then(response => {
      //         if (response.data.error_code === 0) {
      //           alert('添加成功')
      //           this.resetForm(formName)
      //           this.pageList()
      //         } else {
      //           console.log(response.data)
      //         }
      //       })
      //       .catch(function(error) {
      //         console.log(error)
      //       })
      //     this.visible.addDialog = false
      //   } else {
      //     console.log('error submit!!')
      //     return false
      //   }
      // })
    },
    handleEditCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$http
            .post('http://127.0.0.1:8000/api/edit_item', this.editForm)
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
    handleDelete(index, row) {
      // console.log(index, row)
      this.$confirm('此操作将删除此项目, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          this.$http
            .post('http://127.0.0.1:8000/api/delete_item', { item_id: row.item_id })
            .then(response => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                })
                this.pageList()
              }
            })
            .catch(function(error) {
              console.log(error)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    handleEdit(index, row) {
      console.log(index, row)
      this.editForm.introduction = row.item_introduction
      this.editForm.name = row.item_name
      this.editForm.id = row.item_id
      this.visible.editDialog = true
    },
    handleAddBasedExist(formName) {
      this.visible.addDialog2 = true
    }
  }
}
</script>

<style lang="scss" scoped>
.tableTitle {
  height: 634px;
  overflow-y: scroll;
}
</style>
