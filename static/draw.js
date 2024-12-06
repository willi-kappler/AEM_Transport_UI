const TOOL_NONE = 0;
const TOOL_MOVE = 1;
const TOOL_DELETE = 2;
const TOOL_ZOOM_IN = 3;
const TOOL_ZOOM_OUT = 4;
const TOOL_PAN = 5;
const TOOL_CIRCLE = 10;
const TOOL_LINE = 11;

const canvas = document.getElementById("draw_canvas");
const ctx = canvas.getContext("2d");
const handle_size = 5;

var mouse_down = false;
var current_tool = TOOL_NONE
const gfx_elements = [];
const mouse_points = [];
const gfx_undo_buffer = [];

// Buttons:
const btn_clear = document.getElementById("btn_clear");
const btn_delete = document.getElementById("btn_delete");
const btn_move = document.getElementById("btn_move");
const btn_undo = document.getElementById("btn_undo");
const btn_zoom_in = document.getElementById("btn_zoom_in");
const btn_zoom_out = document.getElementById("btn_zoom_out");
const btn_pan = document.getElementById("btn_pan");
const btn_circle = document.getElementById("btn_circle");
const btn_line = document.getElementById("btn_line");

btn_clear.onclick = function() {
    fill_undo_buffer();
    gfx_elements.length = 0;
    change_tool(TOOL_NONE);
    clear_and_redraw();
}

btn_delete.onclick = function() {
    change_tool(TOOL_DELETE);
}

btn_move.onclick = function() {
    change_tool(TOOL_MOVE);
}

btn_undo.onclick = function() {
    if (gfx_undo_buffer.length > 0) {
        change_tool(TOOL_NONE);

        let prev_elements = gfx_undo_buffer.pop();
        gfx_elements.length = 0;
        prev_elements.forEach(element => {
            // Clone each gfx element individually
            gfx_elements.push(element.clone());
        });
        clear_and_redraw();
    }
}

btn_zoom_in.onclick = function() {
    change_tool(TOOL_ZOOM_IN);
}

btn_zoom_out.onclick = function() {
    change_tool(TOOL_ZOOM_OUT);
}

btn_pan.onclick = function() {
    change_tool(TOOL_PAN);
}

btn_circle.onclick = function() {
    change_tool(TOOL_CIRCLE);
}

btn_line.onclick = function() {
    change_tool(TOOL_LINE);
}

class Element_Circle {
    constructor() {
        if (mouse_points.length > 0) {
            let p1x = mouse_points[0][0];
            let p1y = mouse_points[0][1];
            let p2x = mouse_points[1][0];
            let p2y = mouse_points[1][1];
            let dx = p1x - p2x;
            let dy = p1y - p2y;

            this.centerx = p1x;
            this.centery = p1y;
            this.radius = Math.hypot(dx, dy);
        } else {
            // Use default values:
            this.centerx = 0.0;
            this.centery = 0.0;
            this.radius = 0.0;
        }
    }

    draw() {
        draw_circle(this.centerx, this.centery, this.radius);
    }

    mouse_contact(p1x, p1y) {
        return this.center_contact(p1x, p1y) || this.handle_contact(p1x, p1y);
    }

    center_contact(p1x, p1y) {
        let dx = p1x - this.centerx;
        let dy = p1y - this.centery;
        let d = Math.hypot(dx, dy);

        return d <= handle_size;
    }

    handle_contact(p1x, p1y) {
        let dx = p1x - (this.centerx + this.radius);
        let dy = p1y - this.centery;
        let d = Math.hypot(dx, dy);

        return d <= handle_size;
    }

    clone() {
        let result = new Element_Circle();
        result.centerx = this.centerx;
        result.centery = this.centery;
        result.radius = this.radius;

        return result;
    }
}

class Element_Line {
    constructor() {
        if (mouse_points.length > 0) {
            this.p1x = mouse_points[0][0];
            this.p1y = mouse_points[0][1];
            this.p2x = mouse_points[1][0];
            this.p2y = mouse_points[1][1];
        } else {
            // Use default values:
            this.p1x = 0.0;
            this.p1y = 0.0;
            this.p2x = 0.0;
            this.p2y = 0.0;
        }
    }

    draw() {
        draw_line(this.p1x, this.p1y, this.p2x, this.p2y)
    }

    mouse_contact(p1x, p1y) {
        return this.p1_contact(p1x, p1y) || this.p2_contact(p1x, p1y);
    }

    p1_contact(p1x, p1y) {
        let dx = p1x - this.p1x;
        let dy = p1y - this.p1y;
        let d = Math.hypot(dx, dy);

        return d <= handle_size;
    }

    p2_contact(p1x, p1y) {
        let dx = p1x - this.p2x;
        let dy = p1y - this.p2y;
        let d = Math.hypot(dx, dy);

        return d <= handle_size;
    }

    clone() {
        let result = new Element_Line();
        result.p1x = this.p1x;
        result.p1y = this.p1y;
        result.p2x = this.p2x;
        result.p2y = this.p2y;

        return result;
    }
}

canvas.onmousedown = function(e) {
    mouse_down = true;
}

canvas.onmouseup = function(e) {
    if (mouse_down) mouse_click(e);
    mouse_down = false;
}

canvas.onmousemove = function(e) {
    num_points = mouse_points.length

    if (mouse_down) {
        // Used for the move tool
        if (current_tool == TOOL_MOVE) {
            // TODO: implement
        }
    } else {
        switch (current_tool) {
            case TOOL_CIRCLE:
                if (num_points == 1) {
                    let p1x = mouse_points[0][0];
                    let p1y = mouse_points[0][1];
                    let p2x = e.offsetX;
                    let p2y = e.offsetY;
                    let dx = p1x - p2x;
                    let dy = p1y - p2y;
                    let radius = Math.hypot(dx, dy)

                    clear_and_redraw();
                    draw_circle(p1x, p1y, radius);
                }
                break;
            case TOOL_LINE:
                if (num_points == 1) {
                    let p1x = mouse_points[0][0];
                    let p1y = mouse_points[0][1];
                    let p2x = e.offsetX;
                    let p2y = e.offsetY;

                    clear_and_redraw();
                    draw_line(p1x, p1y, p2x, p2y);
                }
                break;
        }
    }
}

function mouse_click(e) {
    num_points = mouse_points.length

    switch (current_tool) {
        case TOOL_DELETE:
            let del_index = -1
            let p1x = e.offsetX;
            let p1y = e.offsetY;
            let num_elems = gfx_elements.length;

            for (let i = 0; i < num_elems; i++) {
                if (gfx_elements[i].mouse_contact(p1x, p1y)) {
                    del_index = i;
                    break;
                }
            }

            if (del_index >= 0) {
                fill_undo_buffer();
                gfx_elements.splice(del_index, 1);
                clear_and_redraw();
                change_tool(TOOL_NONE);
            }

            break;
        case TOOL_CIRCLE:
            if (num_points == 0) {
                mouse_points.push([e.offsetX, e.offsetY]);
            } else if (num_points == 1) {
                mouse_points.push([e.offsetX, e.offsetY]);
                fill_undo_buffer();
                let new_circle = new Element_Circle();
                gfx_elements.push(new_circle);
                mouse_points.length = 0;
                clear_and_redraw();
            }
            break;
        case TOOL_LINE:
            if (num_points == 0) {
                mouse_points.push([e.offsetX, e.offsetY]);
            } else if (num_points == 1) {
                mouse_points.push([e.offsetX, e.offsetY]);
                fill_undo_buffer();
                let new_line = new Element_Line();
                gfx_elements.push(new_line);
                mouse_points.length = 0;
                clear_and_redraw();
            }
            break;
    }

}

function change_tool(tool) {
    mouse_points.length = 0;
    mouse_down = false;

    switch (current_tool) {
        case TOOL_MOVE:
            btn_move.classList.toggle("active");
        break;
        case TOOL_DELETE:
            btn_delete.classList.toggle("active");
        break;
        case TOOL_PAN:
            btn_pan.classList.toggle("active");
        break;
        case TOOL_CIRCLE:
            btn_circle.classList.toggle("active");
        break;
        case TOOL_LINE:
            btn_line.classList.toggle("active");
        break;
    }

    if (tool == current_tool) {
        current_tool = TOOL_NONE;
        return
    }

    current_tool = tool;

    switch (current_tool) {
        case TOOL_MOVE:
            btn_move.classList.toggle("active");
        break;
        case TOOL_DELETE:
            btn_delete.classList.toggle("active");
        break;
        case TOOL_PAN:
            btn_pan.classList.toggle("active");
        break;
        case TOOL_CIRCLE:
            btn_circle.classList.toggle("active");
        break;
        case TOOL_LINE:
            btn_line.classList.toggle("active");
        break;
    }
}

function fill_undo_buffer() {
    objs = Array.from(gfx_elements);
    gfx_undo_buffer.push(objs);

    if (gfx_undo_buffer.length > 50) {
        // If undo list gets too big remove first element (= oldest entry)
        gfx_undo_buffer.shift();
    }
}

function clear_and_redraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    gfx_elements.forEach(element => {
        element.draw();
    });
}

function draw_circle(p1x, p1y, radius) {
    // Draw outline:
    ctx.beginPath();
    ctx.arc(p1x, p1y, radius, 0, 2 * Math.PI);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "black";
    ctx.stroke();

    // Draw center:
    ctx.beginPath();
    ctx.arc(p1x, p1y, handle_size, 0, 2 * Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();

    // Draw radius handle:
    ctx.beginPath();
    ctx.arc(p1x + radius, p1y, handle_size, 0, 2 * Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();
}

function draw_line(p1x, p1y, p2x, p2y) {
    // Draw the line:
    ctx.beginPath();
    ctx.moveTo(p1x, p1y);
    ctx.lineTo(p2x, p2y);
    ctx.lineWidth = 2;
    ctx.strokeStyle = "black";
    ctx.stroke();

    // Draw handle 1:
    ctx.beginPath();
    ctx.arc(p1x, p1y, handle_size, 0, 2 * Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();

    // Draw handle 2:
    ctx.beginPath();
    ctx.arc(p2x, p2y, handle_size, 0, 2 * Math.PI);
    ctx.fillStyle = "red";
    ctx.fill();
}

