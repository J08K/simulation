import { Dispatch, SetStateAction } from "react"

export type Species = {
    id: 0,
    name: string,
    prey: number[],
    can_move: boolean,
    can_see: boolean,
}

export type Gene = {
    uuid: string,
    name: string,
    value: number,
    mutability: number,
}

export type Genome = {
    uuid: string,
    gender: string, // TODO Change this into an enum.
    genes: Gene[],
}

export type LongTermMemory = {
    memory_length: number,
    static_food_locations: Array<{
        time_added: number,
        x: number,
        y: number,
    }>,
}

export type ShortTermMemory = {
    memory_length: number,
    entity_locations: Array<{
        uuid: string,
        time_added: number,
        x: number,
        y: number,
    }>,
}

export type Memory = {
    current_time: number,
    short_term: ShortTermMemory,
    long_term: LongTermMemory,
}

export type Entity = {
    uuid: string,
    species: Species,
    genome: Genome,
    memory: Memory,
    is_alive: boolean,
}

export type EntityLocation = {
    entity : Entity,
    x : number,
    y : number,
}

export type BoardProps = {
    width : number,
    height : number,
    grid_size : number,
    entity_locations : Array<EntityLocation>,
    onEntitySelect: Function,
}

export type EntityListProps = {
    entity_locations : Array<EntityLocation>,
    setEntityLocations : Dispatch<SetStateAction<EntityLocation[]>>,
}

export let test_entity_location : EntityLocation = {
    entity: {
        uuid: "026e156e-8747-4094-a5f9-2142cfd9c5fa",
        species: {
            id: 0,
            name: "TEST",
            prey: [1, 2, 3, 4, 5, 6],
            can_move: true,
            can_see: false,
        },
        genome: {
            uuid: "a5b7467d-0f1e-4935-b5d2-f3bfb18d6d2c",
            gender: "FEMALE",
            genes: [
                {
                    uuid: "77ccca7d-3dd0-4325-9ce6-1ae830ecd5bc",
                    name: "speed",
                    value: 0.5,
                    mutability: 0.1,
                },
                {
                    uuid: "844b756a-6ecc-41e9-9516-a36427db5571",
                    name: "hunger_rate",
                    value: 0.4,
                    mutability: 0.1,
                },
            ]
        },
        memory: {
            current_time: 2.1,
            short_term: {
                memory_length: 3,
                entity_locations: [{
                    uuid: "885a88a4-900f-414f-89bf-0c9dbe58b20e",
                    time_added: 0.1,
                    x: 1,
                    y: 1,
                }],
            },
            long_term: {
                memory_length: 4,
                static_food_locations: [{
                    time_added: 0.1,
                    x: 2,
                    y: 2,
                }],
            }
        },
        is_alive: false,
    },
    x: 2,
    y: 2,
}