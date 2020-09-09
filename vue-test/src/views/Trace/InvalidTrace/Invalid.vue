<template>
  <div>
    <el-card>
      <el-input v-model="search" placeholder="输入关键字搜索" style="float: right;width: 300px" />
      <el-table border :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))" style="width: 100%">
        <el-table-column type="index" label="Id" width="50"> </el-table-column>
        <el-table-column property="name" label="名称" width="120"> </el-table-column>
        <el-table-column property="transition" label="失效序列"> </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
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
      search: ''
    }
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row)
    },
    handleDelete(index, row) {
      console.log(index, row)
    }
  }
}
</script>
