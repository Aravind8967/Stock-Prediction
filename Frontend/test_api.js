async function testSharePrice(c_name, future_years){
    const url = `http://127.0.0.1:8080/${c_name}/getSharePrice/${future_years}`
    const response = await fetch(url)
    if(response.ok){
        const result = await response.json()
        console.log(result)
    }
    else{
        console.log('URL not found')
    }
}

async function testFundamentals(c_name, future_years) {
    const url = `http://127.0.0.1:8080/${c_name}/getFundamentals/${future_years}`
    const response = await fetch(url)
    if(response.ok){
        const result = await response.json()
        console.log(result)
    }
    else{
        console.log('url not found')
    }
}