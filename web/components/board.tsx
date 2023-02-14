import styles from "./board.module.scss";

import { BoardProps } from "../utils/types";

function genGrids(width: number, height: number, grid_size: number) {
    let num_width_full_grids = Math.floor(width / grid_size);
    let num_height_full_grids = Math.floor(height / grid_size);

    let width_column_partial_grids = width % grid_size;
    let height_row_partial_grids = height % grid_size;

    let sub_grids: Array<JSX.Element> = [];
    let grid_num = 0;
    let row_num = 0;

    let first_row_height = ((1 / num_height_full_grids) * 100).toString() + "%";

    if (height_row_partial_grids > 0) {
        first_row_height = "auto";

        let row: Array<JSX.Element> = [];
        for (let idx = 0; idx < num_width_full_grids; idx++) {
            row.push(
                <td key={grid_num} style={{width: "auto"}}></td>
            );
            grid_num++;
        }

        if (width_column_partial_grids > 0) {
            row.push(
                <td key={grid_num} style={{width: ((width_column_partial_grids / height) * 100).toString() + "%"}}></td>
            );
            grid_num++;
        }

        sub_grids.push(
            <thead style={{height : ((height_row_partial_grids / height) * 100).toString() + "%"}} key={grid_num.toString() + "-" + row_num.toString()}><tr>{...row}</tr></thead>
        );
        grid_num++;
        row_num++;
    }

    for (let idx = 0; idx < num_height_full_grids; idx++) {
        let row : Array<JSX.Element> = [];
        for (let edx = 0; edx < num_width_full_grids; edx++) {
            row.push(
                <td key={grid_num} style={{width : "auto", height : "auto"}}></td>
            );
            grid_num++;
        }

        if (width_column_partial_grids > 0) {
            row.push(
                <td key={grid_num} style={{"width" : ((width_column_partial_grids / height) * 100).toString() + "%", height: "auto"}}></td>
            );
            grid_num++;
        }
        sub_grids.push(
            <thead style={{height: idx === 0 ? first_row_height : "auto"}}key={grid_num.toString() + "-" + row_num.toString()}><tr>{...row}</tr></thead>
        )
        row_num++;

    }

    return sub_grids;
}

const Board = (props : BoardProps) => {

    return (
        <div className={styles.board}>
            <div className={styles.base_grid} style={{"aspectRatio" : `${props.width}/${props.height}`}}>
                <table id="sub_grids"> { genGrids(props.width, props.height, props.grid_size) } </table>
                <div id="entities"></div>
            </div>
        </div>
    );
}

export default Board;