describe 'database' do
  before do
    `rm ruby_unit_test.db`
  end

  def run_script(commands)
    raw_output = nil
    IO.popen("./nwodb ruby_unit_test.db", "r+") do |pipe|
      commands.each do |command|
        pipe.puts command
      end

      pipe.close_write

      # Read entire output
      raw_output = pipe.gets(nil)
    end
    raw_output.split("\n")
  end

  it 'inserts and retreives a row' do
    result = run_script([
      "insert 1 user1 person1@example.com",
      "select",
      ".exit",
    ])
    expect(result).to match_array([
      "nwodb > executed",
      "nwodb > (1, user1, person1@example.com)",
      "executed",
      "nwodb > ",
    ])
  end

  # it 'prints error message when table is full' do
  #   script = (1..1401).map do |i|
  #     "insert #{i} user#{i} person#{i}@example.com"
  #   end
  #   script << ".exit"
  #   result = run_script(script)
  #   expect(result[-2]).to eq('nwodb > Error: Table full.')
  # end

  it 'allows inserting strings that are the maximum length' do
    long_username = "a"*32
    long_email = "a"*255
    script = [
      "insert 1 #{long_username} #{long_email}",
      "select",
      ".exit",
    ]
    result = run_script(script)
    expect(result).to match_array([
      "nwodb > executed",
      "nwodb > (1, #{long_username}, #{long_email})",
      "executed",
      "nwodb > ",
    ])
  end

  it 'prints error message if strings are too long' do
    long_username = "a"*33
    long_email = "a"*256
    script = [
      "insert 1 #{long_username} #{long_email}",
      "select",
      ".exit",
    ]
    result = run_script(script)
    expect(result).to match_array([
      "nwodb > Error: String is too long.",
      "nwodb > executed",
      "nwodb > ",
    ])
  end

  it 'prints an error message if id is negative' do
    script = [
      "insert -1 my_name foo@bar.com",
      "select",
      ".exit",
    ]
    result = run_script(script)
    expect(result).to match_array([
      "nwodb > Error: ID must be a positive integer.",
      "nwodb > executed",
      "nwodb > ",
    ])
  end

  it 'prints an error message if id is a string' do
    script = [
      "insert foo my_name foo@bar.com",
      "select",
      ".exit",
    ]
    result = run_script(script)
    expect(result).to match_array([
      "nwodb > Error: ID must be a positive integer.",
      "nwodb > executed",
      "nwodb > ",
    ])
  end

  it 'keeps data after closing connection' do
    result1 = run_script([
      "insert 1 user1 person1@example.com",
      ".exit",
    ])
    expect(result1).to match_array([
      "nwodb > executed",
      "nwodb > ",
    ])
    result2 = run_script([
      "select",
      ".exit",
    ])
    expect(result2).to match_array([
      "nwodb > (1, user1, person1@example.com)",
      "executed",
      "nwodb > ",
    ])
  end

  it 'allows printing out the structure of a 3-leaf-node btree' do
    script = (1..14).map do |i|
      "insert #{i} user#{i} person#{i}@example.com"
    end
    script << ".btree"
    script << "insert 15 user15 person15@example.com"
    script << ".exit"
    result = run_script(script)

    expect(result[14...(result.length)]).to match_array([
      "nwodb > Tree:",
      "- internal (size 1)",
      "  - leaf (size 7)",
      "    - 1",
      "    - 2",
      "    - 3",
      "    - 4",
      "    - 5",
      "    - 6",
      "    - 7",
      "  - key 7",
      "  - leaf (size 7)",
      "    - 8",
      "    - 9",
      "    - 10",
      "    - 11",
      "    - 12",
      "    - 13",
      "    - 14",
      "nwodb > Need to implement searching an internal node",
    ])
  end

  it 'prints constants' do
    script = [
      ".constants",
      ".exit",
    ]
    result = run_script(script)

    expect(result).to match_array([
      "nwodb > Constants:",
      "ROW_SIZE: 293",
      "COMMON_NODE_HEADER_SIZE: 6",
      "LEAF_NODE_HEADER_SIZE: 10",
      "LEAF_NODE_CELL_SIZE: 297",
      "LEAF_NODE_SPACE_FOR_CELLS: 4086",
      "LEAF_NODE_MAX_CELLS: 13",
      "nwodb > ",
    ])
  end

  it 'prints an error message if there is a duplicate id' do
    script = [
      "insert 1 user1 person1@example.com",
      "insert 1 user1 person1@example.com",
      "select",
      ".exit",
    ]
    result = run_script(script)
    expect(result).to match_array([
      "nwodb > executed",
      "nwodb > Error: Duplicate key.",
      "nwodb > (1, user1, person1@example.com)",
      "executed",
      "nwodb > ",
    ])
  end


  it 'gets the constants of a b-tree' do
    script = (5..17).map do |i|
      "insert #{i} user#{i} person#{i}@example.com"
    end

    script << ".exit"
    result = run_script(script)
  end

end