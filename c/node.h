#ifndef NODE_H_
#define NODE_H_

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "row.h"

enum NodeType_t { NODE_INTERNAL, NODE_LEAF };
typedef enum NodeType_t NodeType;

/*
 * Common Node Header Layout
 */
#define NODE_TYPE_SIZE          sizeof(uint8_t)                                         // uint32_t
#define IS_ROOT_SIZE            sizeof(uint8_t)                                         // uint32_t
#define PARENT_POINTER_SIZE     sizeof(uint32_t)                                        // uint32_t
#define COMMON_NODE_HEADER_SIZE (NODE_TYPE_SIZE + IS_ROOT_SIZE + PARENT_POINTER_SIZE)   // uint8_t 

#define NODE_TYPE_OFFSET        (0)                                                     // uint32_t
#define IS_ROOT_OFFSET          (NODE_TYPE_SIZE)                                        // uint32_t
#define PARENT_POINTER_OFFSET   (IS_ROOT_OFFSET + IS_ROOT_SIZE)                         // uint32_t

/*
 * Leaf Node Header Layout
 */
#define LEAF_NODE_NUM_CELLS_SIZE   sizeof(uint32_t)                                     // uint32_t
#define LEAF_NODE_NUM_CELLS_OFFSET (COMMON_NODE_HEADER_SIZE)                            // uint32_t
#define LEAF_NODE_HEADER_SIZE      (COMMON_NODE_HEADER_SIZE + LEAF_NODE_NUM_CELLS_SIZE) // uint32_t

/*
 * Leaf Node Body Layout
 */
#define LEAF_NODE_KEY_SIZE        sizeof(uint32_t)                                      // uint32_t
#define LEAF_NODE_VALUE_SIZE      (ROW_SIZE)                                            // uint32_t
#define LEAF_NODE_CELL_SIZE       (LEAF_NODE_KEY_SIZE + LEAF_NODE_VALUE_SIZE)           // uint32_t

#define LEAF_NODE_KEY_OFFSET      (0)                                                   // uint32_t
#define LEAF_NODE_VALUE_OFFSET    (LEAF_NODE_KEY_OFFSET + LEAF_NODE_KEY_SIZE)           // uint32_t
#define LEAF_NODE_SPACE_FOR_CELLS (PAGE_SIZE - LEAF_NODE_HEADER_SIZE)                   // uint32_t

#define LEAF_NODE_MAX_CELLS       (LEAF_NODE_SPACE_FOR_CELLS / LEAF_NODE_CELL_SIZE)     // uint32_t

uint32_t* leaf_node_num_cells(void* node);
void* leaf_node_cell(void* node, uint32_t cell_num);
uint32_t* leaf_node_key(void* node, uint32_t cell_num);
void* leaf_node_value(void* node, uint32_t cell_num);
void initialize_leaf_node(void* node);
NodeType get_node_type(void* node);
void set_node_type(void* node, NodeType type);
uint32_t leaf_node_find_index(void* node, uint32_t key);

#endif /*NODE_H_*/