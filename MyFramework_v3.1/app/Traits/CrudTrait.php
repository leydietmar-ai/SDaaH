<?php

/**
 * Framework 3.1
 *
 * /app/Traits/CrudTrait.php - Change, Read, Update, Delete (CRUD)  T R A I T
 */


namespace App\Traits;

use App\Core\Database;

trait CrudTrait
{
    /**
     * Ermittelt den Primärschlüssel (Standard 'id', falls im Model nicht anders definiert)
     */
    private function getPrimaryKey(): string
    {
        return $this->primaryKey ?? 'id';
    }

    /**
     * Findet einen Datensatz nach Primärschlüssel
     */
    public function find(int $id): ?array
    {
        $db = Database::getInstance();
        $pk = $this->getPrimaryKey();
        $stmt = $db->prepare("SELECT * FROM {$this->table} WHERE {$pk} = :id");
        $stmt->execute(['id' => $id]);
        $result = $stmt->fetch();
        return $result ?: null;
    }

    /**
     * Holt alle Datensätze einer Tabelle
     */
    public function all(): array
    {
        $db = Database::getInstance();
        $stmt = $db->query("SELECT * FROM {$this->table}");
        return $stmt->fetchAll();
    }

    /**
     * Löscht einen Datensatz nach Primärschlüssel
     */
    public function delete(int $id): bool
    {
        $db = Database::getInstance();
        $pk = $this->getPrimaryKey();
        $stmt = $db->prepare("DELETE FROM {$this->table} WHERE {$pk} = :id");
        return $stmt->execute(['id' => $id]);
    }

    /**
     * Erstellt einen neuen Datensatz
     */
    public function create(array $data): bool
    {
        $db = Database::getInstance();
        $columns = implode(', ', array_keys($data));
        $placeholders = ':' . implode(', :', array_keys($data));

        $sql = "INSERT INTO {$this->table} ($columns) VALUES ($placeholders)";
        $stmt = $db->prepare($sql);
        return $stmt->execute($data);
    }

    /**
     * Aktualisiert einen Datensatz
     */
    public function update(int $id, array $data): bool
    {
        $db = Database::getInstance();
        $pk = $this->getPrimaryKey();

        $fields = "";
        foreach ($data as $key => $value) {
            $fields .= "$key = :$key, ";
        }
        $fields = rtrim($fields, ", ");

        $sql = "UPDATE {$this->table} SET $fields WHERE {$pk} = :pk_id";

        // Ich nutze :pk_id, um Konflikte zu vermeiden, falls 'id' auch in $data vorkommt
        $data['pk_id'] = $id;

        return $db->prepare($sql)->execute($data);
    }
}
