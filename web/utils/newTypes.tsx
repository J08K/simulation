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