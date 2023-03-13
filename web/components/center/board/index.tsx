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

function getEntityColor(species_id : number) {

    function hslToHex(h: number, s: number, l: number ) { // Adapted from: https://stackoverflow.com/a/44134328
        l /= 100;
        const a = s * Math.min(l, 1 - l) / 100;
        const f = (n: number) => {
            const k = (n + h / 30) % 12;
            const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
            return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
        };
        return `#${f(0)}${f(8)}${f(4)}`;
    }

    let hue = (species_id % 10) * 100;
    let saturation = 100;
    let lumin = 50;
    
    return hslToHex(hue, saturation, lumin);

}

const EntityBlob = (props : {
    entity: EntityLocation,
    left_offset: number,
    top_offset: number,
    onSelect: Function,
    is_selected: boolean,
}) => {

    return (
        <div onClick={() => {props.onSelect(props.entity)}} style={{left: `${props.left_offset}%`, top: `${props.top_offset}%`, backgroundColor: props.is_selected ? "white" : getEntityColor(props.entity.entity.species.id)}}>{props.entity.entity.species.id}</div>
    )
}

const Board = (props : {
    board_data: Board | null | undefined
    onEntitySelect: Function,
    selected_entity: string | null,
    dimensions : {width: number, height: number, grid_size: number} | null
}) => {

    // ! Do not use for accurate data. 
    var board_width = props.dimensions ? props.dimensions.width : 16
    var board_height = props.dimensions ? props.dimensions.height : 10
    var board_grid_size = props.dimensions ? props.dimensions.grid_size : 3

    function renderEntity(entity_location : EntityLocation, index : number) {
        let reference_grid = document.getElementById("sub_grids");

        if (!reference_grid) {
            throw "Sub grids not found!"
        }

        let top_offset = (1 - (entity_location.y / board_height))  * 100;
        let left_offset = (entity_location.x / board_width) * 100;
        return <EntityBlob key={index} entity={entity_location} left_offset={left_offset} top_offset={top_offset} onSelect={props.onEntitySelect} is_selected={entity_location.entity.uuid === props.selected_entity}/>
    }   

    function renderAllEntities() {
        if (props.board_data) {
            return props.board_data.entities.map((entity_location, index) => renderEntity(entity_location, index))
        }
        return []
    }

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