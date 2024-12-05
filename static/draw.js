const TOOL_NONE = 0;
const TOOL_MOVE = 1;
const TOOL_DELETE = 2;
const TOOL_CIRCLE = 10;
const TOOL_LINE = 11;

const canvas = document.getElementById("draw_canvas");
const ctx = canvas.getContext("2d");

var mouse_down = false;
var current_tool = TOOL_NONE
const gfx_elements = [];
const mouse_points = [];

class Element_Circle {
    constructor() {
        let p1x = mouse_points[0][0];
        let p1y = mouse_points[0][1];
        let p2x = mouse_points[1][0];
        let p2y = mouse_points[1][1];
        let dx = p1x - p2x;
        let dy = p1y - p2y;

        this.centerx = p1x;
        this.centery = p1y;
        this.radius = Math.hypot(dx, dy);
    }
}

class Element_Line {
    constructor() {
        this.startx = mouse_points[0][0];
        this.starty = mouse_points[0][1];
        this.endx = mouse_points[1][0];
        this.endy = mouse_points[1][1];
    }
}

canvas.onmousedown = function(e){
    //dragOffset.x = e.x - mainLayer.trans.x;
    //dragOffset.y = e.y - mainLayer.trans.y;
    mouse_down = true;
}

canvas.onmouseup = function(e){
    if (mouse_down) mouse_click(e);
    mouse_down = false;
}

canvas.onmousemove = function(e){
    //if (!mouse_down) return;

    //mainLayer.trans.x = e.x - dragOffset.x;
    //mainLayer.trans.y = e.y - dragOffset.y;
    //return false;

    num_points = mouse_points.length

    if (mouse_down) {
        // Used for the move tool
    } else {
        switch (current_tool) {
            case TOOL_NONE:
                break;
            case TOOL_MOVE:
                break;
            case TOOL_DELETE:
                break;
            case TOOL_CIRCLE:
                break;
            case TOOL_LINE:
                break;
            default:
                // Nothing to do
        }
    }
}

function mouse_click(e) {
    num_points = mouse_points.length

    switch (current_tool) {
        case TOOL_NONE:
            break;
        case TOOL_MOVE:
            break;
        case TOOL_DELETE:
            break;
        case TOOL_CIRCLE:
            if (num_points == 0) {
                mouse_points.push([e.offsetX, e.offsetY]);
            } else if (num_points == 1) {
                mouse_points.push([e.offsetX, e.offsetY]);
                let new_circle = new Element_Circle();
                gfx_elements.push(new_circle);
                mouse_points.length = 0;
            }
            break;
        case TOOL_LINE:
            if (num_points == 0) {
                mouse_points.push([e.offsetX, e.offsetY]);
            } else if (num_points == 1) {
                mouse_points.push([e.offsetX, e.offsetY]);
                let new_line = new Element_Line();
                gfx_elements.push(new_line);
                mouse_points.length = 0;
            }
            break;
        default:
            console.log("Unknown tool: %s", current_tool)
    }

}

