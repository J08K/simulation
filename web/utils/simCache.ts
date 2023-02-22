import type { SimData } from "./types";

function getNumDecimals(n : number) {
    return (n % 1).toString().substring(2).length;
}

function round(val : number, num_decimals : number) {
    return Math.round(val * Math.pow(10, num_decimals)) / Math.pow(10, num_decimals);
}

async function fetcher (url : string, params: RequestInit = {}) : Promise<SimData | null> {
    return fetch(url, params).then((res) => res.json()).then((data : {sim_data : SimData | null}) => data.sim_data);
}

export type SimCache = {
    high : number,
    low : number,
}

export class SimDataCache {
    private lock : boolean;
    private size : number;

    private time : number;
    private accuracy : number;
    private time_delta : number;
    private collection : string;

    low : number;
    high : number;

    private cache : (SimData | null)[];

    constructor(size : number, collection : string) {
        this.size = size;
        this.lock = false;

        this.time = -1;
        this.accuracy = -1;
        this.time_delta = -1;
        this.collection = collection;

        this.low = -2;
        this.high = -2;

        this.cache = [];

        this.setTimeDelta();
    }

    url(time : number) : string {
        return `/api/database/collections/${this.collection}/${time}`
    }

    setTimeDelta() {
        fetcher(this.url(this.time)).then((data : SimData | null) => {
            if (data) {
                this.time_delta = data.time_delta;
                this.accuracy = getNumDecimals(data.time_delta);
            }
        })
    }

    setCache(current_sim : SimData | null) {

        var cur : number;

        let queue : Array<{
            data : Promise<SimData | null>,
            time : number,
        }> = [];
        let num_items = Math.floor((this.size - 1) / 2);
        let diff = num_items / Math.pow(10, this.accuracy);
        let new_low = round(this.time - diff, this.accuracy);

        for (let idx = new_low; idx < this.time; idx = idx+this.time_delta) {
            if (idx >= 0 && idx != this.time) {
                cur = round(idx, this.accuracy);
                console.log(cur)
                if (cur > this.high && (cur < this.low || this.low < 0) ) {
                    queue.push({
                        data: fetcher(this.url(cur)),
                        time: cur,
                    });
                    console.log(`Downloading: ${cur}`);
                }
            }
        }

        queue.push({
            data: new Promise<SimData | null>((resolve) => {resolve(current_sim)}),
            time: this.time,
        });

        num_items = Math.ceil((this.size - 1) / 2);
        diff = num_items / (Math.pow(10, this.accuracy))
        let new_high = round(this.time + diff, this.accuracy);
        for (let idx = this.time+this.time_delta; idx <= new_high; idx = idx+this.time_delta) {
            cur = round(idx, this.accuracy);
            if (cur > this.high && (cur < this.low || this.low > 0)) {
                queue.push({
                    data: fetcher(this.url(cur)),
                    time: cur,
                });
                console.log(`Downloading: ${cur}`);
            }
        }

        queue.sort((a, b) => a.time - b.time);

        let cur_time : number;
        let old_cache = this.cache.filter((_value, index) => {
            cur_time = round(index / Math.pow(10, this.time_delta), this.accuracy);
            if (cur_time <= this.high && cur_time >= this.low) {
                return true;
            } else {
                return false;
            }
        });

        let new_cache: (SimData | null)[] = this.high >= new_low && this.low <= new_high ? old_cache : [];

        queue.forEach(async (item) => {
            new_cache.push(await item.data)
        });

        if (this.low >= new_low && this.low <= new_high) {
            new_cache = new_cache.concat(old_cache);
        }

        this.low = new_low;
        this.high = new_high;

        this.cache = new_cache;
    }

    async get(time : number, callback : Function) {
        var current_sim : SimData | null = null;

        this.time = time;

        if (!this.lock) {
            this.lock = true;
            if (time >= this.low && time <= this.high) {
                current_sim = this.cache[(time - this.low) * this.accuracy]
            } else {
                current_sim = await fetcher(this.url(time));
            }
            //this.setCache(current_sim);
            this.lock = false;

            callback(current_sim);
        } else {
            setTimeout(this.get, 100, [time, callback]);
        }
    }

    length() {
        return this.cache.length;
    }

    get_all() {
        return this.cache;
    }
}