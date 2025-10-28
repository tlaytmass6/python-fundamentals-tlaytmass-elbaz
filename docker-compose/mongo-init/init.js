// mongo-init/init.js
db = db.getSiblingDB("admin");

// create app user for the application database
db.createUser({
  user: "webuser",
  pwd: "WebPass!789",
  roles: [{ role: "readWrite", db: "classdb" }]
});

const app = db.getSiblingDB("classdb");

app.users.insertMany([
  {
    username: "jana",
    email: "jana@example.com",
    profile: {
      first_name: "Jana",
      last_name: "Moreau",
      age: 26,
      addresses: [
        { street: "12 Rue du Parc", city: "Nice", country: "FR" }
      ]
    },
    roles: ["student"],
    created_at: new Date()
  },
  {
    username: "marc",
    email: "marc@example.org",
    profile: {
      first_name: "Marc",
      last_name: "Silva",
      age: 31,
      addresses: [
        { street: "5 Cedar Ln", city: "Porto", country: "PT" }
      ]
    },
    roles: ["admin","student"],
    created_at: new Date()
  }
]);
