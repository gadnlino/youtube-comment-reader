export function OK(result: any, withLog: boolean = false){
    const r : any = {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if(result != null && result != undefined){
        r.body = JSON.stringify(result);
    }

    if(withLog){
        console.log("Payload retornado:");
        console.log(r)
    }

    return r;
}

export function InternalServerError(result: any, withLog: boolean = false){
    const r : any = {
        statusCode: 500,
        error: result
    };

    if(withLog){
        console.log("Payload retornado:");
        console.log(r)
    }

    return r;
}

export function BadRequest(result: any, withLog: boolean = false){
    let r: any = {
        statusCode: 400,
        
    };
    
    if(result){
        r.body = JSON.stringify(result)
    }

    if(withLog){
        console.log("Payload retornado:");
        console.log(r)
    }

    return r;
}

export function NotFound(result: any = null, withLog: boolean = false){
    const r : any = {
        statusCode: 404,
    };

    if(result){
        r.body = JSON.stringify({error: result});
    }

    if(withLog){
        console.log("Payload retornado:");
        console.log(r)
    }

    return r;
}

export function Forbidden(result: any = null, withLog: boolean = false){
    const r : any = {
        statusCode: 403,
    };

    if(result){
        r.body = JSON.stringify({error: result});
    }

    if(withLog){
        console.log("Payload retornado:");
        console.log(r)
    }

    return r;
}