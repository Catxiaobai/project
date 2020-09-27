<template>
  <div id="sample">
    <el-card>
      <!--      <el-button type="primary" @click="save">save</el-button>-->
      <!--      <el-button type="primary" @click="load">load</el-button>-->
      <span style="font-size: x-large;margin-left: 40%">模型可视化</span>
      <div id="myDiagramDiv" style="background-color: whitesmoke; border: solid 1px black; width: 100%; height: 520px;margin-top: 20px"></div>
      <textarea id="myTransaction" style="width:100%;height:200px" v-show="false"></textarea>
    </el-card>

    <br />
  </div>
</template>

<script>
import go from 'gojs'
const MAKE = go.GraphObject.make
export default {
  name: 'PageThree.vue',
  data() {
    return {
      nodeDataArray: [],
      linkDataArray: [],
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: []
      }
    }
  },
  mounted() {
    var $ = go.GraphObject.make
    this.myDiagram = MAKE(go.Diagram, 'myDiagramDiv', {
      // have mouse wheel events zoom in and out instead of scroll up and down
      'toolManager.mouseWheelBehavior': go.ToolManager.WheelZoom,
      // support double-click in background creating a new node
      'clickCreatingTool.archetypeNodeData': { text: 'new node' },
      'undoManager.isEnabled': true,
      // 力导向布局
      // todo: 每次打开后不一致，线交叉，有时经过节点
      layout: $(go.ForceDirectedLayout, {
        defaultSpringLength: 200,
        defaultElectricalCharge: 300
      })
    })
    this.myDiagram.nodeTemplate = MAKE(
      go.Node,
      'Auto',
      {
        cursor: 'pointer',
        // define a tooltip for each node that displays the color as text
        toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'name'))) // end of Adornment
      },
      new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
      // define the node's outer shape, which will surround the TextBlock

      // 图标的style
      MAKE(go.Shape, 'RoundedRectangle', {
        parameter1: 20, // the corner has a large radius
        fill: MAKE(go.Brush, 'Linear', { 0: 'rgb(7, 201, 125)', 1: 'rgb(54, 125, 0)' }),
        stroke: 'black',
        portId: '',
        fromLinkable: true,
        fromLinkableSelfNode: true,
        fromLinkableDuplicates: true,
        toLinkable: true,
        toLinkableSelfNode: true,
        toLinkableDuplicates: true,
        cursor: 'pointer'
      }),
      // 字体的style
      MAKE(
        go.TextBlock,
        {
          font: 'bold 11pt helvetica, bold arial, sans-serif',
          editable: true // editing the text automatically updates the model data
        },
        new go.Binding('text', 'text').makeTwoWay()
      )
    )
    this.myDiagram.toolManager.hoverDelay = 10

    // unlike the normal selection Adornment, this one includes a Button
    this.myDiagram.nodeTemplate.selectionAdornmentTemplate = $(
      go.Adornment,
      'Spot',
      $(
        go.Panel,
        'Auto',
        $(go.Shape, { fill: null, stroke: 'blue', strokeWidth: 2 }),
        $(go.Placeholder) // this represents the selected Node
      ),
      // the button to create a "next" node, at the top-right corner
      $(
        'Button',
        {
          alignment: go.Spot.TopRight,
          click: addNodeAndLink // this function is defined below
        },
        $(go.Shape, 'PlusLine', { desiredSize: new go.Size(6, 6) })
      ) // end button
    ) // end Adornment
    // and adds a link to that new node
    function addNodeAndLink(e, obj) {
      var adorn = obj.part
      e.handled = true
      var diagram = adorn.diagram
      diagram.startTransaction('Add State')

      // get the node data for which the user clicked the button
      var fromNode = adorn.adornedPart
      var fromData = fromNode.data
      // create a new "State" data object, positioned off to the right of the adorned Node
      var toData = { text: 'new' }
      var p = fromNode.location.copy()
      p.x += 200
      toData.loc = go.Point.stringify(p) // the "loc" property is a string, not a Point object
      // add the new node data to the model
      var model = diagram.model
      model.addNodeData(toData)

      // create a link data from the old node data to the new node data
      var linkdata = {
        from: model.getKeyForNodeData(fromData), // or just: fromData.id
        to: model.getKeyForNodeData(toData),
        text: 'transition'
      }
      // and add the link data to the model
      model.addLinkData(linkdata)

      // select the new Node
      var newnode = diagram.findNodeForData(toData)
      diagram.select(newnode)

      diagram.commitTransaction('Add State')

      // if the new node is off-screen, scroll the diagram to show the new node
      diagram.scrollToRect(newnode.actualBounds)
    }
    // replace the default Link template in the linkTemplateMap
    this.myDiagram.linkTemplate = $(
      go.Link, // the whole link panel
      {
        curve: go.Link.Bezier,

        adjusting: go.Link.AvoidsNodes,
        // reshapable: true,
        // relinkableFrom: true,
        // relinkableTo: true,
        // routing: go.Link.AvoidsNodes,
        corner: 36
      },
      {
        cursor: 'pointer',
        // define a tooltip for each node that displays the color as text
        toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'action'))) // end of Adornment
      },
      new go.Binding('points').makeTwoWay(),
      new go.Binding('curviness', 'curviness'),
      $(
        go.Shape, // the link shape
        { strokeWidth: 1.5 }
      ),
      $(
        go.Shape, // the arrowhead
        { toArrow: 'standard', stroke: null }
      ),
      $(
        go.Panel,
        'Auto',
        $(
          go.Shape, // the label background, which becomes transparent around the edges
          {
            fill: $(go.Brush, 'Radial', { 0: 'rgb(240, 240, 240)', 0.3: 'rgb(240, 240, 240)', 1: 'rgba(240, 240, 240, 0)' }),
            stroke: null
          }
        ),
        $(
          go.TextBlock,
          'transition', // the label text
          {
            textAlign: 'center',
            font: '10pt helvetica, arial, sans-serif',
            stroke: 'black',
            margin: 4,
            editable: true // editing the text automatically updates the model data
          },
          new go.Binding('text', 'text').makeTwoWay()
        )
      )
    )
  },
  methods: {
    showIncremental(str) {
      // show the last transaction as an incremental update in JSON-formatted text
      var element = document.getElementById('myTransaction')
      // don't show anything upon the initial layout
      if (element.value === 'InitialLayout') str = ''
      element.value = str
    },
    save() {
      // document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      console.log(this.myDiagram.model.toJson())
      this.text_data = this.myDiagram.model.toJSON()
      this.myDiagram.isModified = false
      this.showIncremental('')
    },
    load() {
      // var model = go.Model.fromJson(document.getElementById('mySavedModel').value)
      // establish GraphLinksModel functions:
      // node data id's are odd numbers
      var model = go.Model.fromJson(this.text_data)
      console.log(this.text_data)
      console.log(model.nodeDataArray)
      // console.log(document.getElementById('mySavedModel').value)
      model.makeUniqueKeyFunction = function(model, data) {
        var i = model.nodeDataArray.length * 2 + 1
        while (model.findNodeDataForKey(i) !== null) i += 2
        data.id = i // assume Model.nodeKeyProperty === "id"

        return i
      }
      // link data id's are even numbers
      model.makeUniqueLinkKeyFunction = function(model, data) {
        var i = model.linkDataArray.length * 2 + 2
        while (model.findLinkDataForKey(i) !== null) i += 2
        data.id = i // assume GraphLinksModel.linkKeyProperty === "id"
        return i
      }
      this.myDiagram.model = model
      this.showIncremental('')
    },
    getData() {
      this.$http
        .get('http://127.0.0.1:8000/api/read_txt')
        .then(response => {
          console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          console.log(this.text_data)
          this.load()
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  },
  created() {
    this.getData()
  }
}
</script>

<style scoped></style>
