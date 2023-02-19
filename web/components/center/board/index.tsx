import { useEffect, useState } from "react";
import styles from "./styling.module.scss";

import { Board, EntityLocation } from "@/utils/types";

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
            <thead style={{height: idx === 0 ? first_row_height : "auto"}} key={grid_num.toString() + "-" + row_num.toString()}><tr>{...row}</tr></thead>
        )
        row_num++;

    }

    return sub_grids;
}

const EntityBlob = (props : {
    entity: EntityLocation,
    left_offset: number,
    top_offset: number,
    onSelect: Function,
}) => {

    return (
        <div onClick={() => {props.onSelect(props.entity)}} style={{left: `calc(${props.left_offset}px - 0.5em)`, top: `calc(${props.top_offset}px - 0.5em)`}}>{props.entity.entity.species.id}</div>
    )
}

const Board = (props : {
    board_data: Board | null | undefined
    onEntitySelect: Function,
}) => {

    // ! Do not use for accurate data. Value is only set after first resize.
    let [dimensions, setDimensions] = useState({width : 0, height : 0});
    let time_out : NodeJS.Timeout;
    let [first_rendered, setFirstRendered] = useState(false);

    var board_width = props.board_data ? props.board_data.width : 16
    var board_height = props.board_data ? props.board_data.height : 10
    var board_grid_size = props.board_data ? props.board_data.grid_size : 3

    function renderEntity(entity_location : EntityLocation, index : number) {
        let reference_grid = document.getElementById("sub_grids");

        if (!reference_grid) {
            throw "Sub grids not found!"
        }

        let reference_width = reference_grid.scrollWidth;
        let reference_height = reference_grid.scrollHeight;

        let top_offset = reference_height - ((reference_height / board_height) * entity_location.y);
        let left_offset = (reference_width / board_width) * entity_location.x;
        return <EntityBlob key={index} entity={entity_location} left_offset={left_offset} top_offset={top_offset} onSelect={props.onEntitySelect}/>
    }   

    function renderAllEntities() {
        if (first_rendered) {
            if (props.board_data) {
                return props.board_data.entities.map((entity_location, index) => renderEntity(entity_location, index))
            }
            else {
                return []
            }
        } else {
            return []
        }
    }

    useEffect(() => {

        if (!first_rendered) {
            setFirstRendered(true)
        }

        function handleResize() { 
            setDimensions({
                width: window.innerWidth,
                height: window.innerWidth,
            })
        }

        function handleResizeEvent(event : Event) {
            if (!time_out) {
                time_out = setTimeout(handleResize, 100);
            }
            clearTimeout(time_out);
            time_out = setTimeout(handleResize, 100);
        }

        window.addEventListener("resize", handleResizeEvent);

        board_width = props.board_data ? props.board_data.width : 16
        board_height = props.board_data ? props.board_data.height : 10
        board_grid_size = props.board_data ? props.board_data.grid_size : 3

        return () => {
            window.removeEventListener("resize", handleResizeEvent);
        }
    });

    return (
        <div className={styles.board}>
            <div className={styles.base_grid} style={{"aspectRatio" : `${board_width}/${board_height}`}}>
                <table id="sub_grids">{ ...genGrids(board_width, board_height, board_grid_size) }</table>
                <div id="entities" className={styles.Entities}>{...renderAllEntities() /* TODO Doesn't rerender correctly, needs refresh */}</div>
            </div>
        </div>
    );
}

export default Board;