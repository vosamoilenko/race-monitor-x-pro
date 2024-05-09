const express = require("express")
const cors = require("cors")
const fs = require("fs")

const app = express()

app.use(
  cors({
    origin: "http://localhost:5173",
    optionsSuccessStatus: 200,
  })
)
app.use(express.json())

const PORT = 3000

// Function to read JSON data
const getData = () => {
  try {
    const jsonData = fs.readFileSync(
      "/Users/vo1/Developer/github.com/vosamoilenko/race-monitor-x-pro/obd-rally-golf/output.json"
    )
    return JSON.parse(jsonData)
  } catch (error) {
    console.error("Error reading the JSON file:", error)
    return []
  }
}

// Route to get data by index
app.get("/data/:id", (req, res) => {
  const data = getData()
  const index = parseInt(req.params.id, 10)

  // Check if the index is within the range of the data array
  if (index >= 0 && index < data.length) {
    res.json(data[index])
  } else {
    res.status(404).send("Data not found")
  }
})

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`)
})
