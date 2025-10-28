db = db.getSiblingDB("admin");

db.createUser({
  user: "webuser",
  pwd: "WebPass!789",
  roles: [{ role: "readWrite", db: "classdb" }]
});

const app = db.getSiblingDB("classdb");

app.users.insertMany([
  {
    username: "lina",
    email: "lina@example.com",
    profile: {
      first_name: "lina",
      last_name: "Moreau",
      age: 24,
      addresses: [
        { street: "12 Rue du Parc", city: "Nantes", country: "FR" }
      ]
    },
    roles: ["student"],
    created_at: new Date()
  },
  {
    username: "rayane",
    email: "rayane@example.org",
    profile: {
      first_name: "Rayane",
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
