// Step 2:
// use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
db.authors.find()
db.books.find()

// Step 6: insert two new books
db.books.insertMany([
   {
     title: "Emma",
     published_year: 1815,
     author_ids: ["author_001"]
   },
   {
     title: "The Left Hand of Darkness",
     published_year: 1969,
     author_ids: ["author_004"]
   }
 ])

// Step 7: add missing authors
db.authors.insertOne({
   _id: "author_004",
   name: "Ursula K. Le Guin",
   nationality: "American",
   bio: {
     short: "Ursula K. Le Guin (1929–2018) was an acclaimed American author whose science fiction and fantasy works, including The Left Hand of Darkness and the Earthsea series, explored themes of culture, power, gender, and human society.",
     long: "Ursula K. Le Guin was an American novelist, poet, and essayist widely regarded as one of the most influential writers of science fiction and fantasy. Through works such as The Left Hand of Darkness, The Dispossessed, and the Earthsea series, she used imaginative worlds to examine social, political, and philosophical questions. Her writing earned numerous awards and helped expand the literary recognition of speculative fiction."
   }
})

// Step 8: filter books by a list of authors
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })