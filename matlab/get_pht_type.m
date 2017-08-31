function [ pht_type ] = get_pht_type( file_name )
pht_type = [];
pht_type_list = {'numerical', 'in_vitro_type1', 'in_vitro_type2', 'in_vitro_type3'};
for kk = 1:numel(pht_type_list)
    if contains(file_name, pht_type_list{kk})
        pht_type = pht_type_list{kk};
        break
    end
end

end

