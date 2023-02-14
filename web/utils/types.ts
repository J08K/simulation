export type Entity = {
    id : number
}

export type EntityLocation = {
    entity : Entity,
    x : number,
    y : number,
}

export type BoardProps = {
    width : number;
    height : number;
    grid_size : number;
    entity_locations : Array<EntityLocation>
}

export type EntityListProps = {
    
}