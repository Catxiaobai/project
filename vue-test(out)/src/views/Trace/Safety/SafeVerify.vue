<template>
  <div>
    <el-card>
      <el-table ref="singleTable" :data="tableData" @row-click="handdle" highlight-current-row @current-change="handleCurrentChange" style="width: 100%">
        <el-table-column type="index" label="Id" width="50"> </el-table-column>
        <el-table-column property="name" label="名称" width="120"> </el-table-column>
        <el-table-column property="transition" label="失效序列"> </el-table-column>
      </el-table>
      <el-dialog title="提示" :visible.sync="showDialog" width="30%">
        <span>是否选择 {{ transName }} 进行验证</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="showDialog = false">取 消</el-button>
          <el-button type="primary" @click="verify">确 定</el-button>
        </span>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showDialog: false,
      transName: '',
      trans: '',
      tableData: [
        {
          name: '失效序列1',
          transition:
            'name=T33\n' +
            'src=S1\n' +
            'tgt=S1\n' +
            'event=Enter_pin(p)\n' +
            'cond=!(p!=pin,attempts=0)\n' +
            'action=Write("Wrong Pin,ReEnter"),attempts=attempts+1'
        },
        {
          name: '失效序列2',
          transition: 'name=T34\n' + 'src=S3\n' + 'tgt=S4\n' + 'event=Enter_amount(w)\n' + 'cond=!(w<=B)\n' + 'action=Give_money,B=B-w,Write("your balance",B)'
        },
        {
          name: '失效序列3',
          transition: 'name=T27\n' + 'src=S3\n' + 'tgt=Exit\n' + 'event=Enter_amount(w)\n' + 'cond=!(w>B)\n' + 'action=Write("Out balance")'
        },
        {
          name: '失效序列4',
          transition:
            'name=T40\n' +
            'src=S1\n' +
            'tgt=S2\n' +
            'event=Enter_pin(p)\n' +
            'cond=!(p=pin,attempts=2)\n' +
            'action=Write("Select Withdrawal/GetBalance/Cancel"),attempts=attempts+1'
        },
        {
          name: '失效序列5',
          transition:
            'name=T67\n' +
            'src=S1\n' +
            'tgt=S1\n' +
            'event=Enter_pin(p)\n' +
            'cond=!(p!=pin,attempts=1)\n' +
            'action=Write("Wrong Pin,ReEnter"),attempts=attempts+1'
        },
        {
          name: '失效序列6',
          transition: 'name=T62\n' + 'src=S2\n' + 'tgt=S4\n' + 'event=GetBalance()\n' + 'cond= \n' + 'action=Write("your balance",B)'
        }
      ],
      currentRow: null
    }
  },
  methods: {
    handdle(row) {
      console.log(row)
      this.transName = row.name
      this.trans = row.transition
      this.showDialog = true
    },
    handleCurrentChange(val) {
      this.currentRow = val
    },
    verify() {
      this.showDialog = false
      this.$http
        .post('http://127.0.0.1:8000/api/safe_verify', { msg: this.trans })
        .then(response => {
          console.log({ msg: this.trans })
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped></style>
