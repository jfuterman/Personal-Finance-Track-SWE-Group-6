import React, { useState, useEffect } from "react";
import AddTransactionModal from "../components/AddTransactionModal";
import { useLocation } from "react-router-dom";

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [formOpen, setFormOpen] = useState(false);
  const [editTx, setEditTx] = useState(null);
  const [filters, setFilters] = useState({
    transaction_type: "",
    from_date: "",
    to_date: "",
  });

  useEffect(() => {
    fetch("http://localhost:8000/api/transactions/")
      .then((res) => res.json())
      .then(setTransactions);
  }, []);

  const location = useLocation();
  const search =
    new URLSearchParams(location.search).get("search")?.toLowerCase() || "";

  const normalizeDate = (dateStr) =>
    new Date(dateStr).toISOString().split("T")[0];

  const filtered = transactions.filter((tx) => {
    const txDate = new Date(tx.date).toLocaleDateString("en-CA"); // 'YYYY-MM-DD'
    const fromDate = filters.from_date;
    const toDate = filters.to_date;
  
    const matchType = filters.transaction_type
      ? tx.transaction_type === filters.transaction_type
      : true;
  
    const matchFrom = fromDate ? txDate >= fromDate : true;
    const matchTo = toDate ? txDate <= toDate : true;
  
    const matchSearch = search
      ? tx.item_name.toLowerCase().includes(search) ||
        tx.shop_name.toLowerCase().includes(search) ||
        tx.category?.toLowerCase().includes(search)
      : true;
  
    return matchType && matchFrom && matchTo && matchSearch;
  });

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this transaction?")) {
      fetch(`http://localhost:8000/api/transactions/${id}/`, {
        method: "DELETE",
      }).then(() => {
        setTransactions((prev) => prev.filter((tx) => tx.id !== id));
      });
    }
  };

  return (
    <div className="w-full px-6">
      <div className="flex justify-between items-center mb-5">
        <h2 className="text-2xl fw-semibold">Recent Transactions</h2>
        <button
          onClick={() => setFormOpen(true)}
          className="btn btn-primary bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow"
        >
          + Add Transaction
        </button>
      </div>

      {/* Filters Card */}
      <div className="rounded-lg bg-white shadow p-4 mb-6">
        <form className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">
              Transaction Type
            </label>
            <select
              value={filters.transaction_type}
              onChange={(e) =>
                setFilters({ ...filters, transaction_type: e.target.value })
              }
              className="form-select w-full border rounded px-3 py-2"
            >
              <option value="">All Types</option>
              <option value="expense">Expense</option>
              <option value="revenue">Revenue</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">From Date</label>
            <input
              type="date"
              value={filters.from_date}
              onChange={(e) =>
                setFilters({ ...filters, from_date: e.target.value })
              }
              className="form-control w-full border rounded px-3 py-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">To Date</label>
            <input
              type="date"
              value={filters.to_date}
              onChange={(e) =>
                setFilters({ ...filters, to_date: e.target.value })
              }
              className="form-control w-full border rounded px-3 py-2"
            />
          </div>
          <div className="flex items-end gap-2">
            <button
              type="submit"
              className="btn btn-primary bg-blue-600 text-white px-4 py-2 rounded"
            >
              Apply Filters
            </button>
            <button
              type="button"
              className="btn btn-outline-secondary border border-gray-400 px-4 py-2 rounded"
              onClick={() =>
                setFilters({ transaction_type: "", from_date: "", to_date: "" })
              }
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      {/* Table */}
      <div className="rounded-lg bg-white shadow p-4 overflow-x-auto">
        <table className="table-auto w-full text-sm border-t">
          <thead className="text-left bg-gray-100">
            <tr>
              <th className="px-4 py-2">Date</th>
              <th className="px-4 py-2">Type</th>
              <th className="px-4 py-2">Item</th>
              <th className="px-4 py-2">Shop</th>
              <th className="px-4 py-2">Amount</th>
              <th className="px-4 py-2">Payment</th>
              <th className="px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan="7" className="text-center py-4">
                  No transactions found.
                </td>
              </tr>
            ) : (
              filtered.map((tx) => (
                <tr
                  key={tx.id}
                  className="border-t hover:bg-gray-100 cursor-pointer"
                  onClick={() => setEditTx(tx)}
                >
                  <td className="px-4 py-2">
                    {new Date(tx.date).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-2">
                    <span
                      className={`badge text-white text-xs px-2 py-1 rounded ${
                        tx.transaction_type === "expense"
                          ? "bg-red-500"
                          : "bg-green-500"
                      }`}
                    >
                      {tx.transaction_type}
                    </span>
                  </td>
                  <td className="px-4 py-2">{tx.item_name}</td>
                  <td className="px-4 py-2">{tx.shop_name}</td>
                  <td className="px-4 py-2">
                    ${parseFloat(tx.amount).toFixed(2)}
                  </td>
                  <td className="px-4 py-2">
                    {typeof tx.payment_method === "string"
                      ? tx.payment_method
                          .replace(/_/g, " ")
                          .replace(/\b\w/g, (l) => l.toUpperCase())
                      : "—"}
                  </td>
                  <td className="px-4 py-2">
                    <button
                      onClick={() => handleDelete(tx.id)}
                      className="btn btn-sm text-red-600 hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {(formOpen || editTx) && (
        <AddTransactionModal
          mode={editTx ? "edit" : "add"}
          transaction={editTx}
          onClose={() => {
            setFormOpen(false);
            setEditTx(null);
          }}
          onAdd={(newTx) => {
            if (editTx) {
              // Replace edited transaction
              setTransactions((prev) =>
                prev.map((t) => (t.id === newTx.id ? newTx : t))
              );
            } else {
              // Add new transaction
              setTransactions((prev) => [...prev, newTx]);
            }
          }}
        />
      )}
    </div>
  );
}
